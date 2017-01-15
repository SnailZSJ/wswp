# -*- coding: utf-8 -*-

import xlsxwriter
import re
from datetime import datetime
from bs4 import BeautifulSoup
from link_crawler import link_crawler
from db_psql import WswpDb
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class ScrapeCallback:
    def __init__(self):
        self.workbook = xlsxwriter.Workbook('movie.xlsx')
        self.writer = self.workbook.add_worksheet('豆瓣主页电影')
        self.html_fields = ['链接', '影片', '年份', '封面', '导演', '编剧', '主演', '类型', '制片国家地区', '语言',
                            '上映日期', '季数', '集数', '片长', '又名', '官方网站', '官方小站', 'IMDb链接', '豆瓣评分',
                            '评分人数', '五星', '四星', '三星', '二星', '一星']
        self.tb_fields = ['movie_link', 'movie_name', 'year', 'image', 'director', 'screenwriter', 'actor', 'type',
                          'country', 'language', 'release_date', 'seasons', 'series', 'duration', 'alias', 'website',
                          'official_station', 'IMDb_link', 'douban_score', 'score_peo_num', 'five_star', 'four_star',
                          'three_star', 'two_star', 'one_star']
        self.writer.write_row(0, 0, self.html_fields)
        self.col = 1

        wswpdb = WswpDb()
        date_str = datetime.strftime(datetime.now(), '%Y-%m-%d')
        self.tb_name = ('movie_' + date_str).replace("-", "_")
        tb_fields = (',').join([field + ' VARCHAR(255)' for field in self.tb_fields])
        wswpdb.create_wswp_db(self.tb_name, tb_fields)

    def __call__(self, url, html):
        if re.search('/subject/', url):
            tree = BeautifulSoup(html, 'lxml')
            content = tree.find("div", id="content")

            # 标题
            name_and_year = [item.get_text() for item in content.find("h1").find_all("span")]
            name, year = name_and_year if len(name_and_year) == 2 else (name_and_year[0], "")
            movie = [url, name.strip().encode('utf-8').replace('\'', '\'\''), year.strip("()").encode('utf-8')]

            # 左边
            content_left = tree.find("div", class_="subject clearfix")

            nbg_tree = content_left.find("a", class_="nbgnbg").find("img")
            movie.append(nbg_tree.get("src").encode('utf-8') if nbg_tree else "")

            info = content_left.find("div", id="info").get_text()
            info_dict = dict(
                [line.encode('utf-8').strip().split(":", 1) for line in info.strip().split("\n") if line.strip().find(":") > 0])

            movie.append(info_dict.get("导演", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("编剧", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("主演", "").replace("\t", " ").replace('\'', '\'\''))

            movie.append(info_dict.get("类型", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("制片国家/地区", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("语言", "").replace("\t", " ").replace('\'', '\'\''))

            movie.append(info_dict.get("上映日期", "").replace("\t", " ").replace('\'', '\'\'') if "上映日期" in info_dict else info_dict.get("首播", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("季数", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("集数", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("片长", "").replace("\t", " ").replace('\'', '\'\'') if "片长" in info_dict else info_dict.get("单集片长", "").replace("\t", " ").replace('\'', '\'\''))

            movie.append(info_dict.get("又名", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("官方网站", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("官方小站", "").replace("\t", " ").replace('\'', '\'\''))
            movie.append(info_dict.get("IMDb链接", "").replace("\t", " ").replace('\'', '\'\''))

            # 右边
            content_right = tree.find("div", class_="rating_wrap clearbox")
            if content_right:
                movie.append(content_right.find("strong", class_="ll rating_num").get_text().encode('utf-8').replace('\'', '\'\''))

                rating_people = content_right.find("a", class_="rating_people")
                movie.append(rating_people.find("span").get_text().encode('utf-8').replace('\'', '\'\'') if rating_people else "")

                if content_right.find_all("span", class_="rating_per"):
                    movie.extend([item.get_text().encode('utf-8').replace('\'', '\'\'') for item in content_right.find_all("span", class_="rating_per")])
                else:
                    movie.extend(["", "", "", "", ""])
            else:
                movie.extend(["", "", "", "", "", "", ""])

            assert len(movie) == 25, "length of movie is invalid"
            self.writer.write_row(self.col, 0, movie)
            self.col += 1

            tb_movie = str(tuple([field.decode('utf-8') for field in movie])).replace('u\'','\'').decode("unicode-escape")
            wswpdb = WswpDb()
            wswpdb.insert_wswp_db(self.tb_name, (',').join(self.tb_fields), tb_movie)


if __name__ == '__main__':
    link_crawler('http://movie.douban.com', '/subject/', scrape_callback=ScrapeCallback())

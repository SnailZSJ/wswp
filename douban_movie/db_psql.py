# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import AsIs
import logging


class WswpDb:

    def __init__(self):
        self.db_name = "wswp"
        self.db_user = "jack"
        self.db_pass = "123456"
        self.db_ip = "localhost"
        self.error_log = "scrape_error"
        self.port = 5432

        # 定义日志输出格式
        logging.basicConfig(level=logging.ERROR,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename=self.error_log,
                            filemode='a')

    def create_wswp_db(self, tb_name=None, tb_fields=None):
        """
        连接mysql数据库（写），并进行增的操作，如果连接失败，会把错误写入日志中，并返回false，
        如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
        """
        if tb_name and tb_fields:
            try:
                # 连接数据库
                conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_pass, host=self.db_ip, port=self.port)
                # 建立游标
                cursor = conn.cursor()
            except Exception, e:
                print e
                logging.error('数据库连接失败:%s' % e)
                return False
            try:
                # 执行SQL语句
                cursor.execute("SELECT tablename FROM pg_tables;")
                tb_names = cursor.fetchall()
                if tuple([tb_name]) in tb_names:
                    pass
                else:
                    cursor.execute("""CREATE TABLE {0} (id SERIAL, {1});""".format(tb_name, tb_fields))
                    # 提交事务
                    conn.commit()
            except Exception, e:
                conn.rollback()   # 如果出错，则事务回滚
                logging.error('数据写入失败:%s' % e)
                return False
            finally:
                # 关闭
                cursor.close()
                conn.close()
            return True
        return False

    def insert_wswp_db(self, table, fields, values):
        """
        连接mysql数据库（写），并进行写的操作，如果连接失败，会把错误写入日志中，并返回false，
        如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
        """
        try:
            # 连接数据库
            conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_pass, host=self.db_ip, port=self.port)
            # 建立游标
            cursor = conn.cursor()
        except Exception, e:
            print e
            logging.error('数据库连接失败:%s' % e)
            return False
        try:
            # 执行SQL语句
            cursor.execute("""INSERT INTO {0} ({1}) VALUES {2};""".format(table, fields, values))
            # 提交事务
            conn.commit()
        except Exception, e:
            conn.rollback()   # 如果出错，则事务回滚
            logging.error('数据写入失败:%s' % e)
            return False
        finally:
            # 关闭
            cursor.close()
            conn.close()
        return True

    def update_wswp_db(self, sql):
        """
        连接mysql数据库（写），并进行写的操作，如果连接失败，会把错误写入日志中，并返回false，
        如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回true
        """
        if 'UPDATE' in sql:
            try:
                # 连接数据库
                conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_pass, host=self.db_ip, port=self.port)
                # 建立游标
                cursor = conn.cursor()
            except Exception, e:
                print e
                logging.error('数据库连接失败:%s' % e)
                return False
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 提交事务
                conn.commit()
            except Exception, e:
                conn.rollback()   # 如果出错，则事务回滚
                logging.error('数据写入失败:%s' % e)
                return False
            finally:
                # 关闭
                cursor.close()
                conn.close()
            return True
        else:
            return False

    def read_wswp_db(self, sql):
        """
        连接mysql数据库（从），并进行数据查询，如果连接失败，会把错误写入日志中，并返回false，
        如果sql执行失败，也会把错误写入日志中，并返回false，如果所有执行正常，则返回查询到的数据，
        这个数据是经过转换的，转成字典格式，方便模板调用，其中字典的key是数据表里的字段名
        """
        if 'SELECT' in sql:
            try:
                # 连接数据库
                conn = psycopg2.connect(database=self.db_name, user=self.db_user, password=self.db_pass, host=self.db_ip, port=self.port)
                # 建立游标
                cursor = conn.cursor()
            except Exception, e:
                print e
                logging.error('数据库连接失败:%s' % e)
                return False
            try:
                # 执行SQL语句
                cursor.execute(sql)
                # 转换数据，字典格式
                data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            except Exception, e:
                logging.error('数据执行失败:%s' % e)
                return False
            finally:
                # 关闭
                cursor.close()
                conn.close()
            return data
        else:
            return False

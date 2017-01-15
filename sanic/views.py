from .exceptions import InvalidUsage


class HTTPMethodView:
    """ Simple class based implementation of view for the sanic.
    You should implement methods (get, post, put, patch, delete) for the class
    to every HTTP method you want to support.

    For example:
        class DummyView(HTTPMethodView):

            def get(self, request, *args, **kwargs):
                return text('I am get method')

            def put(self, request, *args, **kwargs):
                return text('I am put method')
    etc.

    If someone tries to use a non-implemented method, there will be a
    405 response.

    If you need any url params just mention them in method definition:
        class DummyView(HTTPMethodView):

            def get(self, request, my_param_here, *args, **kwargs):
                return text('I am get method with %s' % my_param_here)

    To add the view into the routing you could use
        1) app.add_route(DummyView.as_view(), '/')
        2) app.route('/')(DummyView.as_view())

    To add any decorator you could set it into decorators variable
    """

    decorators = []

    def dispatch_request(self, request, *args, **kwargs):
        handler = getattr(self, request.method.lower(), None)
        if handler:
            return handler(request, *args, **kwargs)
        raise InvalidUsage(
            'Method {} not allowed for URL {}'.format(
                request.method, request.url), status_code=405)

    @classmethod
    def as_view(cls, *class_args, **class_kwargs):
        """ Converts the class into an actual view function that can be used
        with the routing system.

        """
        def view(*args, **kwargs):
            self = view.view_class(*class_args, **class_kwargs)
            return self.dispatch_request(*args, **kwargs)

        if cls.decorators:
            view.__module__ = cls.__module__
            for decorator in cls.decorators:
                view = decorator(view)

        view.view_class = cls
        view.__doc__ = cls.__doc__
        view.__module__ = cls.__module__
        return view

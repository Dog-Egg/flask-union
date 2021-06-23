import functools

from flask import Flask, abort


class FlaskUnion:
    def __init__(self, app: Flask):
        self.app = app
        self.sep = '+'

    def route(self, prefix: str, functions, **options):
        rule = prefix + '/<names>'

        def decorator(view_func):
            self.app.add_url_rule(rule, view_func=self._wrapper(view_func, functions), **options)
            return view_func

        return decorator

    def _wrapper(self, view_func, functions):
        if not isinstance(functions, dict):
            functions = {f.__name__: f for f in functions}

        @functools.wraps(view_func)
        def decorator(names: str):
            names = names.split(self.sep)

            if [n for n in names if n not in functions]:
                return abort(404)

            result = {n: functions[n]() for n in names}
            return view_func(result)

        return decorator

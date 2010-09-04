# -*- coding: utf-8 -*-
from tipfy import Rule, import_string


def get_rules(app):
    """Returns a list of URL rules for the application. The list can be
    defined entirely here or in separate ``urls.py`` files.

    :param app:
        The WSGI application instance.
    :return:
        A list of class:`tipfy.Rule` instances.
    """
    rules = [
        Rule('/', endpoint='blog/index', handler='apps.blog.staticcontent.handlers.StaticContentHandler'),
        Rule('/<path:path>', endpoint='blog/show_post', handler='apps.blog.staticcontent.handlers.StaticContentHandler'),
    ]

    return rules
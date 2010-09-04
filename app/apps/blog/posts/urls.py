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
        #Rule('/', endpoint='home', handler='apps.blog.posts.admin.handlers.HomeHandler'),
        Rule('/admin/', endpoint='admin/index', handler='apps.blog.posts.admin.handlers.AdminHandler'),
        Rule('/admin/newpost/', endpoint='admin/newpost', handler='apps.blog.posts.admin.handlers.PostHandler'),
        Rule('/admin/post/<int:post_id>', endpoint='admin/post', handler='apps.blog.posts.admin.handlers.PostHandler'),
    ]

    return rules

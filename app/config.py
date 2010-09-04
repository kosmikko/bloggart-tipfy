# -*- coding: utf-8 -*-
"""
    config
    ~~~~~~

    Configuration settings.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE for more details.
"""
config = {}

# Configurations for the 'tipfy' module.
config['tipfy'] = {
    # Enable debugger. It will be loaded only in development.
    'middleware': [
        'tipfy.ext.debugger.DebuggerMiddleware',
    ],
    # Enable the Hello, World! app example.
    'apps_installed': [
        #'apps.blog.auth',
        'apps.blog.posts',
        'apps.blog.staticcontent',         
    ],
}

config['tipfy.ext.session'] = {
    'secret_key': 'XXXXXXXXXXXXXXX',
}

config['tipfy.ext.jinja2'] = {
    'engine_factory': 'apps.blog.filters.create_environment',
} 
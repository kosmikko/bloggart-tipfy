# -*- coding: utf-8 -*-
"""
    urls
    ~~~~

    URL definitions.

    :copyright: 2009 by tipfy.org.
    :license: BSD, see LICENSE.txt for more details.
"""
from tipfy import Rule, import_string


def get_rules(app):

    # http://www.tipfy.org/docs/api/tipfy.ext.taskqueue.html
    rules = [
      Rule('/_ah/queue/deferred', endpoint='tasks/deferred',
       handler='tipfy.ext.taskqueue:DeferredHandler'),
    ]

    for app_module in app.get_config('tipfy', 'apps_installed'):
        try:
            # Load the urls module from the app and extend our rules.
            app_rules = import_string('%s.urls' % app_module)
            rules.extend(app_rules.get_rules(app))
        except ImportError:
            pass

    return rules

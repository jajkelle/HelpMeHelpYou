# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('admin', 'default', 'design/%s' % request.application))
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('admin', 'default', 'design/%s' % request.application))
]

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Resources'), False, '#', [
            (T('View'), False, URL('welcome', 'default', 'view_resource')),
            (T('Add'), False,
             URL(
                 'welcome', 'default', 'add_resource')),
            (T('Delete'), False,
             URL(
                 'welcome', 'default', 'edit/%s/models/db.py' % _app)),
            (T('Edit'), False,
             URL(
                 'welcome', 'default', 'edit/%s/models/db.py' % _app)),
        ]),
        (T('Index'), False, URL('welcome', 'default', 'index')),
    ]
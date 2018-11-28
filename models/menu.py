# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Resources'), False, '#', [
            (T('View'), False,
             URL('test', 'default', 'view_resource')),
            (T('Add'), False,
             URL(
                 'test', 'default', 'add_resource')),
            (T('Delete'), False,
             URL(
                 'test', 'default', 'delete_resource')),
            (T('Edit'), False,
             URL(
                 'test', 'default', 'edit/%s/models/db.py' % _app)),
            (T('Search'), False,
             URL(
                 'test', 'default', 'search_resource')),
        ]),
        (T('Admin'), False, URL('admin', 'default', 'design/%s' % _app)),
    ]

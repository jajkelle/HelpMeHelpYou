# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('admin', 'default', 'design/%s' % request.application))
]

if session.auth:
    user_id = session.auth.user.id
else:
    user_id = None

# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

if not configuration.get('app.production'):
    _app = request.application
    response.menu += [
        (T('Resources'), False, '#', [
            (T('View My Resources'), False, URL('welcome', 'default', 'view_my_resource', args = user_id)),
            (T('View All Resources'), False, URL('welcome', 'default', 'view_resource',  args = user_id)),
            (T('Add Resources'), False,
             URL(
                 'welcome', 'default', 'add_resource',  args = user_id)),
            (T('Delete Resources'), False,
             URL(
                 'welcome', 'default', 'delete_resource',  args = user_id)),
            (T('Edit Resources'), False,
             URL(
                 'welcome', 'default', 'edit_resource', args = user_id)),
        ]),
        (T('Index'), False, URL('welcome', 'default', 'index')),
    ]

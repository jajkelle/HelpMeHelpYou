# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]
if session.auth:
    user_id = session.auth.user.id
else:
    user_id = None

response.menu += [
    (T('Resources'), False,'#', [
      (T('My Resource'), False,URL('list_resources',args = user_id) if session.auth else URL('default','index')),
      ((T('Add Resources'), False, URL('add_resources') if session.auth else URL('default','index'))),
      (T('List Users'), False, URL('list_id')),
        (T('Delete Resources'), False, URL('delete_resource',args = user_id) if session.auth else URL('default','index')),
        (T('Category'),False,URL('category'))]
    )
]
# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

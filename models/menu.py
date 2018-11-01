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
      (T('View'), False,URL('list_resources',args = user_id)),
      (T('Add'), False, URL('add_resources')),
      (T('Other'), False, URL('list_id'))]
    )
]
# ----------------------------------------------------------------------------------------------------------------------
# provide shortcuts for development. you can remove everything below in production
# ----------------------------------------------------------------------------------------------------------------------

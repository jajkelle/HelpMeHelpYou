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
                                                    (T('View'), False, URL('HelpMeHelpYou', 'default', 'view_resource')),
                                                    (T('Add'), False,
                                                     URL(
                                                         'HelpMeHelpYou', 'default', 'add_resource')),
                                                    (T('Delete'), False,
                                                     URL(
                                                         'HelpMeHelpYou', 'default', 'delete_resource')),
                                                    (T('Edit'), False,
                                                     URL(
                                                         'HelpMeHelpYou', 'default', 'edit/%s/models/db.py' % _app)),
                                                    ]),
                      (T('Index'), False, URL('HelpMeHelpYou', 'default', 'index')),
                      ]

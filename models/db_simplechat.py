db.define_table('chat',
        Field('me_from'),
        Field('me_body', 'text'),
        Field('me_html', 'text')
        )

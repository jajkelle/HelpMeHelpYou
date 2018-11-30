db.define_table('folder',
    Field('name'),
    Field('description','text',default=''),
    Field('keywords','string',length=128,default=''),
    Field('is_open','boolean',default=False),
    Field('created_on','datetime',default=timestamp),
    Field('owned_by',db.auth_user))

db.folder.name.requires=IS_NOT_EMPTY()
db.folder.access_types=['none','read','read/edit']
db.folder.public_fields=['name','description','keywords','is_open']

db.define_table('curr_page',
    Field('folder',db.folder),
    Field('num','integer',default=0),
    Field('locked_on','integer',default=0),
    Field('locked_by','integer',default=0),
    Field('title'),
    Field('body','text',default=''),
    Field('readonly','boolean',default=False),
    Field('comments_enabled','boolean',default=False),
    Field('modified_on','datetime',default=timestamp),
    Field('modified_by',db.auth_user))

db.curr_page.folder.requires=IS_IN_DB(db,'folder.id','%(id)s:%(name)s')
db.curr_page.title.requires=IS_NOT_EMPTY()
db.curr_page.public_fields=['title','body','readonly','comments_enabled']

db.define_table('old_page',
    Field('curr_page',db.curr_page),
    Field('title'),
    Field('body','text',default=''),
    Field('modified_on','datetime',default=timestamp),
    Field('modified_by',db.auth_user))

db.define_table('doc',
    Field('curr_page',db.curr_page),
    Field('title'),
    Field('ffile','upload'),
    Field('uploaded_by',db.auth_user),
    Field('uploaded_on','datetime',default=timestamp))

db.doc.curr_page.requires=IS_IN_DB(db,'curr_page.id','%(id)s:%(title)s')
db.doc.title.requires=IS_NOT_EMPTY()
db.doc.public_fields=['title','ffile']

db.define_table('comments',
    Field('curr_page',db.curr_page),
    Field('posted_on','datetime',default=timestamp),
    Field('author',db.auth_user),
    Field('disabled',default=False),
    Field('body','text',default=''))

db.comments.curr_page.requires=IS_IN_DB(db,'curr_page.id','%(id)s:%(title)s')
db.comments.body.requires=IS_NOT_EMPTY()
db.comments.public_fields=['body']

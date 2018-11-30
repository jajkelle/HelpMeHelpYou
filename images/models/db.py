db = DAL("sqlite://storage.sqlite")

db.define_table('image',
                Field('title', unique=True),
                Field('file', 'upload'),
                format = '%(title)s')

db.define_table('post',
                Field('image_id', 'reference image'),
                Field('author'),
                Field('email'),
                Field('body', 'text'))

db.image.title.requires = IS_NOT_IN_DB(db, db.image.title)
db.post.image_id.requires = IS_IN_DB(db, db.image.id, '%(title)s')
db.post.author.requires = IS_NOT_EMPTY()
db.post.email.requires = IS_EMAIL()
db.post.body.requires = IS_NOT_EMPTY()

db.post.image_id.writable = db.post.image_id.readable = False

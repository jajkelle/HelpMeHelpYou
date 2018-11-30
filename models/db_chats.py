import random
import time; now=time.time()
import datetime;
timestamp=datetime.datetime.today()
today=datetime.date.today()

db.define_table('chat_line',
    Field('username'),
    Field('description','text',default=''),
    Field('created_on','datetime',default=timestamp),
    Field('owned_by',db.auth_user))

db.chat_line.username.requires=IS_NOT_EMPTY()
db.chat_line.access_types=['none','read','read/chat']
db.chat_line.public_fields=['username','description']

db.define_table('message_table',
    Field('chat_line',db.chat_line),
    Field('body','text',default=''),
    Field('posted_on','datetime',default=timestamp),
    Field('posted_by',db.auth_user))

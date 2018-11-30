# -*- coding: utf-8 -*-
db.define_table('persons_group',
   Field('name'),
   Field('description','text',default='No group description'),
   Field('owned_by',db.auth_user),
   Field('is_open','boolean',default=False),
   Field('created_on','datetime',default=timestamp))

db.persons_group.name.requires=IS_NOT_EMPTY()
db.persons_group.acc_types=['none','see','see/join']
db.persons_group.public_fields=['name','description','open']

db.define_table('membership',
   Field('person',db.auth_user),
   Field('persons_group',db.persons_group),
   Field('membership_type',default='regular member'))

db.define_table('membership_request',
   Field('person',db.auth_user),
   Field('persons_group',db.persons_group),
   Field('membership_type',default='regular member'))

db.membership.persons_group.requires=IS_IN_DB(db,'persons_group.id','%(id)s:(name)s')

db.define_table('acc',
   Field('persons_group',db.persons_group),
   Field('table_name'),
   Field('record_id','integer'),
   Field('acc_type'))
db.message_table.body.requires=IS_NOT_EMPTY()





db.acc.persons_group.requires=IS_IN_DB(db,'persons_group.id')
db.acc.acc_type.requires=IS_IN_SET(['read','edit'])

db.define_table('announcement',
   Field('title'),
   Field('body','text',default=''),
   Field('own',db.auth_user),
   Field('to_rss','boolean',default=False),
   Field('posted_on','datetime',default=timestamp),
   Field('expires_on','date',default=today+datetime.timedelta(30)))

db.announcement.title.requires=IS_NOT_EMPTY()
db.announcement.acc_types=['none','read']
db.announcement.public_fields=['title','body','expires_on','to_rss']

db.define_table('ignore_announcement',
   Field('person',db.auth_user),
   Field('announcement',db.announcement))

db.ignore_announcement.announcement.requires=IS_IN_DB(db,'announcement.id')

def get_groups(person_id):
    rows=db(db.persons_group.id==db.membership.persons_group)\
           (db.membership.person==person_id).select()
    rows=[Storage(dict(id=row.persons_group.id,\
                       name=row.persons_group.name,\
                       membership_type=row.membership.membership_type))\
          for row in rows]
    return rows

def is_own(person_id,table_name,record_id):
    if not db.has_key(table_name): return False
    return len(db(db[table_name].id==record_id)(db[table_name].own==person_id).select())

def has_acc(person_id,table_name,record_id,acc_types):
    if not isinstance(acc_types,tuple): acc_types=(acc_types,)
    rows=db(db.acc.table_name==table_name)\
           (db.acc.record_id==record_id)\
           (db.acc.acc_type.belongs(acc_types))\
           (db.acc.persons_group.belongs(g_tuple)).select()
    if not len(rows): return None
    return rows[0]

if len(db(db.persons_group.id>0).select())==0:
    db.persons_group.insert(name='Everybody',description='All registered persons belong to this group',own=1) ## must be group 1

if session.token:
    session.person_id=person_id=int(session.token[0])
    session.person_email=person_email=session.token[1]
    session.person_name=person_name=session.token[2]
    session.groups=groups=get_groups(person_id)
    session.g_tuple=g_tuple=tuple([group.id for group in groups])
    if len(session.groups)==0:
        group_id=db.persons_group.insert(name=person_name,own=person_id,description='This group is just for yourself and for people you want to give access to everything you have access to')
        db.membership.insert(persons_group=1,person=person_id)
        db.membership.insert(persons_group=group_id,person=person_id)
        session.groups=groups=get_groups(person_id)
        session.g_tuple=g_tuple=tuple([group.id for group in groups])
else:
    session.person_id=None
    session.person_email=None
    session.person_name=None
    session.groups=None
    session.g_tuple=None
"""
note g_tuple[0] is always (1), the group everybody
     g_tuple[1] is always the group identified by person_id
"""


def accessible(table_name,acc_types=('read',)):
    return db(db.acc.persons_group.belongs(g_tuple))\
             (db.acc.table_name==table_name)\
             (db.acc.acc_type.belongs(acc_types))\
             (db[table_name].id==db.acc.record_id)

def find_groups(items):
    new_items=[]
    last=None
    for item in items:
        if item.acc.record_id!=last:
            last=item.acc.record_id
            new_items.append(item)
            item.accessible_to=[item.acc.persons_group]
        else:
            new_items[-1].accessible_to.append(item.acc.persons_group)
    return new_items

def redirect_change_permissions(table_name,id):
    redirect(URL(r=request,c='acc',f='change',args=[table_name,id],\
      vars=dict(forward=URL(r=request,f='index'))))

def change_permissions(table_name):
    return A(IMG(_src=URL(r=request,c='static',f='main_images/change_permissions.png')),
      _href=URL(r=request,c='acc',f='change',\
      args=[table_name,request.args[0]],vars=dict(forward=URL(r=request,f='index'))))

groups = db(db.persons_group).select()
g_tuple = [r.persons_group for r in db(db.membership.person==auth.user_id).select()]

if len(g_tuple)<2 and auth.user:
    e = db.persons_group(name='everybody')
    if not e:
        e = db.persons_group.insert(name='everybody')
    else:
        e = e.id
    db.membership.insert(person=auth.user.id,persons_group=e)
    g = db.persons_group.insert(name='%(first_name)s %(last_name)s' % auth.user)
    db.membership.insert(person=auth.user.id,persons_group=g)
    g_tuple = [e,g]
print g_tuple

# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

#https://helpmehelpyou/deafult/list_user_resources/user_id/page
#https://helpmehelpyou/deafult/list_user_resources/category/

# ---- example index page ----
def index():
    return dict(message=T('Welcome to HelpMeHelpYou'))


def list_resources():
    #grabs the user_id from the database and calls the whole row
    user_id = request.args(0,cast=int)
    row=db(db.resources.resource_owner==user_id).select()
    return locals()

def delete_resource():
    #grabs the user_id from the database and calls the delete function on that resource_id item
    user_id = request.args(0,cast=int)
    db(db.resources.resources_id == request.vars.resources_id).delete()
    #show the row
    row = db(db.resources.resource_owner==user_id).select()
    return locals()

def list_id():
    #call the row with the users and show the users
    row = db(db.auth_user).select()
    return locals()

def list_resource_by_category():
    #get the category name and get the categories from the database table
    category_name = request.args(0)
    category=db.category(Name=category_name)
    row = db(db.resources.resources_category==category).select()
    return locals()

def add_resources():
    #get the user_id, make the resource owner the user_id, and add the resource to the database
    user_id = session.auth.user.id
    db.resources.resource_owner.default = user_id
    form = SQLFORM(db.resources).process(next=URL('list_resources', args = user_id))
    return dict(form=form)

def edit_resource():
    #take the fields entered by users and update it in the database
    user_id = request.args(0,cast=int)
    edit_id = request.vars.resources_id
    edit_type = request.vars.resources_type
    edit_qty = request.vars.resources_qty
    try:
        db(db.resources.resources_id == edit_id).update(resources_type = edit_type)
    except:
        pass
    try:
        db(db.resources.resources_id == edit_id).update(resources_qty = edit_qty)
    except:
        pass
    specifications = db(db.resources.resource_owner==user_id).select()
    return locals()

def profile():
    #given function, came with framework
    return dict(form=auth.profile())

def search_resource():
    #creates a form with a the field that the user types in
    form = SQLFORM.factory(Field('title', requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        #split the title by word
        tokens = form.vars.title.split()
        #checks throught the database for the resource type that contains that string
        #reference web2py manual
        query = reduce(lambda a,b:a&b,[db.resources.resources_type.contains(k) for k in tokens])

        #the query goes into the value people which gets returned
        people = db(query).select()
    else:
        people= []
    return dict(form=form,result=people)

def list_single_resource():
    #find the row that corresponds to the resource_id and show it
    resource_id = request.args(0,cast=int)
    row=db(db.resources.resources_id==resource_id).select()
    return locals()

def index_2():
    images = db2().select(db2.image.ALL, orderby=db2.image.title)
    return locals()

def makeThumbnail(db2table,ImageID,size=(150,150)):
    #reference "http://www.web2pyslices.com/slice/show/1387/upload-image-and-make-a-thumbnail"
    try:
        thisImage=db2(db2table.id==ImageID).select()[0]
        import os, uuid
        from PIL import Image
    except: return
    im=Image.open(request.folder + 'image/' + thisImage.mainfile)
    im.thumbnail(size,Image.ANTIALIAS)
    thumbName='image.thumb.%s.jpg' % (uuid.uuid4())
    im.save(request.folder + 'image/' + thumbName,'jpeg')
    thisImage.update_record(thumb=thumbName)
    return locals()

def uploadimage():
    #reference "http://www.web2pyslices.com/slice/show/1387/upload-image-and-make-a-thumbnail"
    db2table = db2.image
    if len(request.args):
        records = db2(db2table.id==request.args[0]).select()
    if len(request.args) and len(records):
        form = SQLFORM(db2table, records[0], deletable=True)
    else:
        form = SQLFORM(db2table)
    if form.accepts(request.vars, session):
        response.flash = 'form accepted'
        makeThumbnail(db2table,form.vars.id,(175,175))
    elif form.errors:
        response.flash = 'form has errors'

    list = crud.select(db2table)
    return dict(form=form)

def show():
    #reference "http://www.web2py.com/books/default/chapter/29/03/overview" the web2py manual
    #get the image from the database and show it
    image = db2.image(request.args(0, cast=int)) or redirect(URL('index_2'))
    db2.post.image_id.default = image.id
    #create a form and take the fields associated with the comment and the picture and add it to the image table
    form = SQLFORM(db2.post)
    if form.process().accepted:
        response.flash = 'your comment is posted'
    comments = db2(db2.post.image_id == image.id).select()
    return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db2)

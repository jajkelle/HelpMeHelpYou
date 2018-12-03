# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

#https://helpmehelpyou/deafult/list_user_resources/user_id/page
#https://helpmehelpyou/deafult/list_user_resources/category/

# ---- example index page ----
#Homepage of our website
def index():
    return dict(message=T('Welcome to HelpYouHelpMe'))

#takes in user_id as argument
#list the resource of the user with that user id
def list_resources():
    user_id = request.args(0,cast=int)
    row=db(db.resources.resource_owner==user_id).select()
    return locals()

#takes in user_id as argument
#Goes through that users resource database and delete the requested resource
def delete_resource():
    user_id = request.args(0,cast=int)
    db(db.resources.resources_id == request.vars.resources_id).delete()
    row = db(db.resources.resource_owner==user_id).select()
    return locals()

#list all the user id in our database
def list_id():
    row = db(db.auth_user).select()
    return locals()

#takes in category as argument
#returns a list of resources that belongs in that category
def list_resource_by_category():
    category_name = request.args(0)
    category=db.category(Name=category_name)
    row = db(db.resources.resources_category==category).select()
    return locals()

#takes in user_id of the user in session
#Return a SQL form for the user to add resources to
#Enter the new resources into data base and redirects user to their own resource page
#If not in session, redirect to homepage
def add_resources():
    user_id = session.auth.user.id
    db.resources.resource_owner.default = user_id
    form = SQLFORM(db.resources).process(next=URL('list_resources',args = user_id))
    return locals()

#takes in user_id of the user in session
#Return a form for user to enter the resource they want to edit
#Enter the information of the resource is now changed in our database
#If not in session, redirect to homepage
def edit_resource():
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

#Adds a profile page
def profile():
    return dict(form=auth.profile())

#User input in a SQLForm to find the resources they are looking for
#Returns a list of all the resources that relates to what the user is looking for
def search_resource():
    form = SQLFORM.factory(Field('title', requires=IS_NOT_EMPTY()))
    if form.accepts(request):
        tokens = form.vars.title.split()
        query = reduce(lambda a,b:a&b,[db.resources.resources_type.contains(k) for k in tokens])
        people = db(query).select()
    else:
        people= []
    return dict(form=form,result=people)

#takes a resource id as input
#return the information of that resource
def list_single_resource():
    resource_id = request.args(0,cast=int)
    row=db(db.resources.resources_id==resource_id).select()
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
    return response.download(request, db)

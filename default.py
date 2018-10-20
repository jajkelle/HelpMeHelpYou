# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----

def get_resources():
    resources_id = request.args(0,cast=int)
    resources = db.resources(id=resources_id)
    if not resources:
        session.flash = 'page not found'
        redirect(URL('index'))
    return resources

def index():
    #rows = db(db.resources.resources_id>0).select()
    rows = db(db.resources).select()
    return locals()

def submit_resources():
    form = SQLFORM(db.resources)
    return dict(form=form)

def view_all_resources():
    rows = db(db.resources.id>0).select()
    return dict(rows=rows)

def view_resource():
    rows = db(db.resources.id>0).select()
    row = rows[1]
    return dict(row=row)
    
def add_resource():
    rows = SQLFORM(db.resources)
    rows.vars.id = db.resources.insert(**dict(rows.vars))
    return dict(rows=rows)

def remove_resource():
    n=0
    rows = db(db.resources.resources_id>0).select()
    rows[n].delete_record()
    return local()
        
#def update_resource():

    
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

to=['mdipierro@cs.depaul.edu','paula@mikrut.org']

def email_user():
    form=SQLFORM(db.email_message,fields=['username','your_email','your_message'])
    if form.accepts(request,session):
       subject='message from '
       email_user(sender=form.vars.your_email,\
                  to=to,\
                  email_message=form.vars.your_message,\
                  subject=subject)
       response.flash='your message has been submitted'
    elif form.errors:
       response.flash='please check the form and try again'
    return dict(form=form)
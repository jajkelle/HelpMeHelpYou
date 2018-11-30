# try something like
import datetime



VALUE="""
This is a message
"""

db.define_table('email_message',
   Field('username', 'reference auth_user'),
   Field('your_email', 'text'),
   Field('your_message','text',default=VALUE),
   Field('timestmp',default=str(datetime.datetime.now())))
   
   
def email_user(sender,to,email_message,subject):
    import smtplib
    fromaddr=sender
    if type(to)==type([]): toaddrs=to
    else: toaddrs=[to]
    msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(fromaddr,", ".join(toaddrs),subject,message)
    server = smtplib.SMTP('localhost:25')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()

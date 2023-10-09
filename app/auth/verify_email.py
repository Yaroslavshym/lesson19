import smtplib
async def sendEmail(FROM, TO, CODE, SERVER):
    
    """this is some test documentation in the function"""
    message = """\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (f'From: Recipes.com, Your code is: {CODE}')
    server = smtplib.SMTP(SERVER)
    server.sendmail(FROM, TO, message)
    server.quit()

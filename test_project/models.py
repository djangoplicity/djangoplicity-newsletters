from django.db import models
from djangoplicity.newsletters.mailers import MailmanMailerPlugin

class SimpleMailer( MailmanMailerPlugin ):
    name = 'Standard mailer'
    # action_run_test = ''

    action_parameters = [
            ('name', 'list name', 'str'),
            ( 'password', 'Admin password for list', 'str' ),
            ( 'somenum', 'Some num', 'int' ),
        ]
    abstract = True

    def __init__(self, *args, **kwargs):
        pass

    # def run( self, conf ):
    #     self.action_run_test = conf
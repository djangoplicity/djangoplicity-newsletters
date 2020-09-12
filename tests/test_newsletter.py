from django.test import TestCase
from djangoplicity.newsletters.models import Mailer, MailerParameter, MailerLog, make_nl_id
from djangoplicity.newsletters.mailers import MailChimpMailerPlugin, MailmanMailerPlugin, EmailMailerPlugin
from test_project.models import SimpleMailer

class MailerTestCase(TestCase):

    def createNewMailer(self):
        Mailer.objects.all().delete()
        m = Mailer(plugin='test_project.models.SimpleMailer', name='Simple Mailer')
        m.register_plugin(SimpleMailer)
        m.save()
        return m
    
    def createNewMailerParameter(self, mailer):
        MailerParameter.objects.all().delete()
        p = MailerParameter.objects.create(mailer=mailer ,name='test', value='value test')
        p.save()
        return p

    def test_list_mailer(self):
        m = self.createNewMailer()
        list_choices = m.get_plugin_choices()
        list_test = [
            (MailChimpMailerPlugin.get_class_path(), MailChimpMailerPlugin.name),
            (MailmanMailerPlugin.get_class_path(), MailmanMailerPlugin.name),
            (EmailMailerPlugin.get_class_path(), EmailMailerPlugin.name),
            (SimpleMailer.get_class_path(), SimpleMailer.name)
        ]
        self.assertEquals(list_choices, list_test )

    def test_get_class_registered(self):
        m = self.createNewMailer()
        self.assertEquals(m.get_plugincls(), SimpleMailer)
    
    def test_get_plugin(self):
        m = self.createNewMailer()
        p = self.createNewMailerParameter(m)
        self.assertIsInstance(m.get_plugin(), SimpleMailer)
    
    def test_get_parameters(self):
        m = self.createNewMailer()
        p = self.createNewMailerParameter(m)
        self.assertEquals(m.get_parameters(), {u'test': u'value test'})

    def test_dispatch(self):
        a = self.createNewMailer()
        p = self.createNewMailerParameter(a)
        #self.assertTrue(SimpleAction.successful())
        a.post_save_handler()

    def test_get_value(self):
        a = self.createNewMailer()
        p = self.createNewMailerParameter(a)
        self.assertEquals(p.get_value(), u'value test')
    
    def test_create_mailerLog(self):
        a = MailerLog(plugin='test_project.tests.SimpleAction', name='Simple action')
        self.assertEquals(a.name, u'Simple action')
    
    def test_get_class_path(self):
        a = self.createNewMailer()
        p = self.createNewMailerParameter(a)
        log = a.get_plugin()
        path = log.get_class_path()
        self.assertEquals(path, SimpleMailer.get_class_path())
    
    def test_get_id(self):
        a = self.createNewMailer()
        self.assertEquals(make_nl_id(), u'1')
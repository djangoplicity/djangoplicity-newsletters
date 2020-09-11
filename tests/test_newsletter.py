from django.test import TestCase
from djangoplicity.newsletters.models import Mailer, MailerParameter, MailerLog, make_nl_id, Newsletter, NewsletterType, MailChimpCampaign, Language
from djangoplicity.newsletters.mailers import MailChimpMailerPlugin, MailmanMailerPlugin, EmailMailerPlugin
from test_project.models import SimpleMailer, SimpleMailChimpMailerPlugin
from django.conf import settings

class MailerTestCase(TestCase):


    def createNewMailerMailChimp(self):
        Mailer.objects.all().delete()
        m = Mailer(plugin='test_project.models.SimpleMailer', name='Simple Mailer')
        m.register_plugin(SimpleMailChimpMailerPlugin)
        m.save()
        return m
    
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
    
    def createNewsletterType(self):
        NewsletterType.objects.all().delete()
        l = self.createLanguage()
        m = self.createNewMailer()
        l.save()
        m.save()
        print Language.objects.all()
        n = NewsletterType.objects.create(
            id=1,
            name='NewsletterType Test',
            slug='slug-test',
            default_from_name='test',
            default_from_email='test@test.com',
            # languages=l
        )
        # n.save()
        # n.languages.add(l)
        return n
    
    def createNewsletter(self, newsletterType):
        Newsletter.objects.all().delete()
        n = Newsletter.objects.create(
            id='slug-test-newsletters',
            type=newsletterType
        )
        return n
    
    def createLanguage(self):
        Language.objects.all().delete()
        l = Language.objects.create(
            lang = settings.LANGUAGE_CODE
        )
        return l

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

    def test_on_scheduled(self):
        a = self.createNewMailerMailChimp()
        nlt = self.createNewsletterType()
        nl = self.createNewsletter(nlt)
        # a.on_scheduled(nl)
        print MailChimpCampaign.objects.all()
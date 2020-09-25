from django.test import TestCase
from djangoplicity.newsletters.models import Mailer, MailerParameter, MailerLog, make_nl_id, Newsletter, NewsletterType, MailChimpCampaign, Language, NewsletterLanguage
from djangoplicity.newsletters.mailers import MailChimpMailerPlugin, MailmanMailerPlugin, EmailMailerPlugin
from test_project.models import SimpleMailer, SimpleMailChimpMailerPlugin
from django.conf import settings

from djangoplicity.mailinglists.models import MailChimpList

class MailerTestCase(TestCase):

    TEST_API_KEY = "78ce5b4dfc49245cacd9fa255acf14d0-us10"
    TEST_LIST_ID = "ed25775a52"

    #
    # Helper methods
    #
    def _valid_list( self ):
        return MailChimpList.objects.create( api_key=self.TEST_API_KEY, list_id=self.TEST_LIST_ID )


    def createNewMailerMailChimp(self):
        Mailer.objects.all().delete()
        m = Mailer(plugin='test_project.models.SimpleMailChimpMailerPlugin', name='Simple MailChimpMailerPlugin')
        m.register_plugin(SimpleMailChimpMailerPlugin)
        m.save()
        return m
    
    def createNewMailer(self):
        Mailer.objects.all().delete()
        m = Mailer(plugin='test_project.models.SimpleMailer', name='Simple Mailer')
        m.register_plugin(SimpleMailer)
        m.save()
        return m
    
    def createNewMailerParameterListId(self, mailer):
        MailerParameter.objects.all().delete()
        p1 = MailerParameter.objects.create(mailer=mailer ,name='list_id', value='ed25775a52')
        p1.save()
        return p1
    
    def createNewMailerParameterEnable_browser_link(self, mailer):
        # MailerParameter.objects.all().delete()
        p = MailerParameter.objects.create(mailer=mailer ,name='enable_browser_link', value=False)
        p.save()
        return p
    
    def createNewsletterLanguage(self, newsletter_type, language):
        NewsletterLanguage.objects.all().delete()
        nll = NewsletterLanguage.objects.create(
            newsletter_type = newsletter_type,
            language = language
        )
        nll.save()
        return nll
    
    def createNewsletterType(self):
        NewsletterType.objects.all().delete()
        l = self.createLanguage()
        m = self.createNewMailer()
        # print Language.objects.all()
        nt = NewsletterType.objects.create(
            id=1,
            name='NewsletterType Test',
            slug='slug-test',
            default_from_name='test',
            default_from_email='test@test.com',
            # languages=l
        )
        nll = self.createNewsletterLanguage(nt, l)
        return nt
    
    def createNewsletter(self, newsletterType):
        Newsletter.objects.all().delete()
        n = Newsletter.objects.create(
            id='1',
            type=newsletterType
        )
        n.save()
        return n
    
    def createLanguage(self):
        Language.objects.all().delete()
        l = Language.objects.create(
            lang = settings.LANGUAGE_CODE
        )
        l.save()
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
        p = self.createNewMailerParameterListId(m)
        self.assertIsInstance(m.get_plugin(), SimpleMailer)
    
    def test_get_parameters(self):
        m = self.createNewMailer()
        p = self.createNewMailerParameterListId(m)
        self.assertEquals(m.get_parameters(), {u'list_id': u'ed25775a52'})

    def test_dispatch(self):
        a = self.createNewMailer()
        p = self.createNewMailerParameterListId(a)
        #self.assertTrue(SimpleAction.successful())
        a.post_save_handler()

    def test_get_value(self):
        a = self.createNewMailer()
        p = self.createNewMailerParameterListId(a)
        self.assertEquals(p.get_value(), u'ed25775a52')
    
    def test_create_mailerLog(self):
        a = MailerLog(plugin='test_project.tests.SimpleAction', name='Simple action')
        self.assertEquals(a.name, u'Simple action')
    
    def test_get_class_path(self):
        a = self.createNewMailer()
        p = self.createNewMailerParameterListId(a)
        log = a.get_plugin()
        path = log.get_class_path()
        self.assertEquals(path, SimpleMailer.get_class_path())
    
    def test_get_id(self):
        a = self.createNewMailer()
        self.assertEquals(make_nl_id(), u'1')

    def test_on_scheduled(self):
        # l = self._valid_list()
        # sm = SimpleMailChimpMailerPlugin()
        a = self.createNewMailerMailChimp()
        nlt = self.createNewsletterType()
        nl = self.createNewsletter(nlt)
        # print a.on_scheduled(nl)

    def test__unicode__(self):
        m = self.createNewMailer()
        self.assertEquals(m.__unicode__(), 'Standard mailer: Simple Mailer')
    
    def test_log_entry(self):
        m = self.createNewMailer()
        nlt = self.createNewsletterType()
        nl = self.createNewsletter(nlt)
        log = m._log_entry(nl)
        self.assertEquals(m.name, 'Simple Mailer')
    
    def test_send_test(self):
        m = self.createNewMailerMailChimp()
        nlt = self.createNewsletterType()
        nl = self.createNewsletter(nlt)
        self.assertEquals(m.send_test(nl), None)

    def test_send_now(self):
        l = self._valid_list()
        l.save()
        print MailChimpList.objects.all()
        nlt = self.createNewsletterType()
        nl = self.createNewsletter(nlt)
        m = self.createNewMailerMailChimp()
        p1 = self.createNewMailerParameterListId(m)
        p2 = self.createNewMailerParameterEnable_browser_link(m)
        # print m.send_now(nl) 
        print m.get_parameters()
        
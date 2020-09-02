from datetime import datetime
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from test_project.settings import NEWSLETTERS_MAILCHIMP_APIKEY

class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@hubble.org',
            password='password123'
        )
        self.client.force_login(self.admin_user)

    # @classmethod
    # def setUpTestData(cls):

    def test_admin_pages_for_models(self):
        """Test that pages for models in admin are properly generated"""
        models = ['bademailaddress', 'subscriber', 'subscription', 'list', 'mailchimplist', 'mailchimplisttoken']
        for model in models:
            url = '/admin/mailinglists/%s/' % model
            res = self.client.get(url)

            self.assertEqual(res.status_code, 200)

    def test_add_list_page(self):
        url = '/admin/mailinglists/mailchimplist/add/'
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)
        self.assertContains(res, NEWSLETTERS_MAILCHIMP_APIKEY)
        self.assertContains(res, "List information")
        self.assertContains(res, "Following information is configured in MailChimp administration interface.")
        # test that contains inline admins
        self.assertContains(res, "Mailchimp merge fields")
        self.assertContains(res, "Mail chimp groups")
        self.assertContains(res, "Mail chimp groupings")
        self.assertContains(res, "Mailchimp merge field mappings")
        self.assertContains(res, "Group mappings")


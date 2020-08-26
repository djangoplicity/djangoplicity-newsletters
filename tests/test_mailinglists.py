from django.test import TestCase, RequestFactory
from mailchimp3 import MailChimp
from django.utils import timezone

TEST_API_KEY = "78ce5b4dfc49245cacd9fa255acf14d0-us10"
TEST_LIST_ID = "ed25775a52"


class ListTest(TestCase):
    LIST_NAME = 'esoepo-monitoring'
    LIST_PASSWORD = 'ohsiechu'
    LIST_BASEURL = 'http://www.eso.org/lists'

    def test_init(self):
        """
        Test creating a list and syncing it with
        """
        from djangoplicity.mailinglists.models import List, Subscriber

        List.objects.all().delete()
        list = List(name=self.LIST_NAME, password=self.LIST_PASSWORD, base_url=self.LIST_BASEURL)
        list.save()

        # Make sure we don't have any subscribers
        Subscriber.objects.all().delete()
        subscriber = Subscriber.objects.create(email='lnielsen@eso.org')
        list.subscribe(subscriber, subscriber.email)

        subscribers = list.subscribers.all()

        self.assertIn(subscriber, subscribers)


class MailChimpListTest(TestCase):
    """
    To ensure that this test runs, you must first manually create
    a mailchimp list, via the web interface.

    When creating the list, please ensure that
      * list name
      * default from name
      * default from email
    fields have a non-blank value (currently they are all required fields)
    """

    #
    # Helper methods
    #
    def _valid_list(self):
        from djangoplicity.mailinglists.models import MailChimpList
        return MailChimpList(api_key=TEST_API_KEY, list_id=TEST_LIST_ID)

    def _invalid_list(self):
        from djangoplicity.mailinglists.models import MailChimpList
        return MailChimpList(api_key="not_valid", list_id="not_valid")

    def _fixture_delete(self, objects):
        for o in objects:
            try:
                o.delete()
            except Exception:
                pass

    def _reset(self):
        from djangoplicity.mailinglists.models import List, Subscriber, Subscription, MailChimpList, MailChimpListToken, \
            MailChimpSourceList, MailChimpSubscriberExclude

        Subscription.objects.all().delete()
        MailChimpListToken.objects.all().delete()
        MailChimpSourceList.objects.all().delete()
        MailChimpSubscriberExclude.objects.all().delete()
        List.objects.all().delete()
        Subscriber.objects.all().delete()
        MailChimpList.objects.all().delete()

    def test_mailchip_list_creation(self):
        list = self._valid_list()
        list.save()

        self.assertEqual(list.connected, True)
        self.assertNotEqual(list.web_id, "")
        self.assertNotEqual(list.name, "")
        self.assertIsNotNone(list.name)
        self.assertNotEqual(list.default_from_name, "")
        self.assertIsNotNone(list.default_from_name)
        self.assertNotEqual(list.default_from_email, "")
        self.assertIsNotNone(list.default_from_email)

        list.delete()

    def test_mailchimp_dc(self):
        from djangoplicity.mailinglists.models import MailChimpList

        list = MailChimpList(api_key="5b9aa23a4e53e80db2de92975de8dd5b-us2", list_id="not_valid")
        self.assertEqual(list.mailchimp_dc(), "us2")

        list = MailChimpList(api_key="5b9aa23a4e53e80db2de92975de8dd5b-us1", list_id="not_valid")
        self.assertEqual(list.mailchimp_dc(), "us1")

        list = MailChimpList(api_key="5b9aa23a4e53e80db2de92975de8dd5b", list_id="not_valid")
        self.assertEqual(list.mailchimp_dc(), "us1")

        list = MailChimpList(api_key=None, list_id=None)
        self.assertIsNone(list.mailchimp_dc())

    def test_connection(self):
        # from djangoplicity.mailinglists.models import MailChimpList
        # Valid api key + list
        # list = self._valid_list()
        # self.assertEqual(list.connection.ping.get(), "Everything's Chimpy!")

        client = MailChimp(mc_api=TEST_API_KEY, mc_user='USER')

        self.assertEqual(client.ping.get()['health_status'], "Everything's Chimpy!")


class MailChimpListTokenTest(TestCase):
    def test_get_token(self):
        from djangoplicity.mailinglists.models import MailChimpList, MailChimpListToken
        from datetime import timedelta

        list = MailChimpList(api_key=TEST_API_KEY, list_id=TEST_LIST_ID, connected=True)
        list.save()

        t = MailChimpListToken.create(list)

        # Valid unexpired token
        t2 = MailChimpListToken.get_token(t.token)
        self.assertNotEqual(t2, None)
        self.assertEqual(t.token, t2.token)
        self.assertEqual(t.uuid, t2.uuid)
        self.assertEqual(t.list, t2.list)
        assert (t.validate_token(list))
        assert (t2.validate_token(list))

        # Expire token, but still valid 10 min after expire date.
        t.expired = timezone.now() - timedelta(minutes=9)
        t.save()

        t2 = MailChimpListToken.get_token(t.token)
        self.assertNotEqual(t2, None)
        self.assertEqual(t.token, t2.token)
        self.assertEqual(t.uuid, t2.uuid)
        self.assertEqual(t.list, t2.list)
        assert (t.validate_token(list))
        assert (t2.validate_token(list))

        # Expire token but now not valid any more.
        t.expired = timezone.now() - timedelta(minutes=11)
        t.save()

        t2 = MailChimpListToken.get_token(t.token)
        self.assertEqual(t2, None)


class WebHooksTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        from djangoplicity.mailinglists.models import MailChimpList, MailChimpListToken
        from urllib import urlencode

        list = MailChimpList(api_key=TEST_API_KEY, list_id=TEST_LIST_ID, connected=True)
        list.save()

        token = MailChimpListToken.create(list)

        self.list = list
        self.token = token
        self.params = urlencode(token.hook_params())

    def _mailchimp_webhook(self, data):
        from djangoplicity.mailinglists.views import mailchimp_webhook
        request = self.factory.post('/webhook/?%s' % self.params, data=data)
        return mailchimp_webhook(request, require_secure=False)

    def test_subscribe(self):
        data = {
            "type": "subscribe",
            "fired_at": "2009-03-26 21:35:57",
            "data[id]": "8a25ff1d98",
            "data[list_id]": self.list.list_id,
            "data[email]": "api@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30",
            "data[ip_signup]": "10.20.10.30",
        }
        response = self._mailchimp_webhook(data)
        self.assertEqual(response.status_code, 200)

    def test_unsubscribe(self):
        data = {
            "type": "unsubscribe",
            "fired_at": "2009-03-26 21:40:57",
            "data[id]": "8a25ff1d98",
            "data[list_id]": self.list.list_id,
            "data[email]": "api+unsub@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api+unsub@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30",
            "data[campaign_id]": "cb398d21d2",
            "data[reason]": "hard"
        }
        response = self._mailchimp_webhook(data)
        self.assertEqual(response.status_code, 200)

    def test_cleaned(self):
        data = {
            "type": "cleaned",
            "fired_at": "2009-03-26 22:01:00",
            "data[list_id]": self.list.list_id,
            "data[campaign_id]": "4fjk2ma9xd",
            "data[reason]": "hard",
            "data[email]": "api+cleaned@mailchimp.com"
        }
        response = self._mailchimp_webhook(data)
        self.assertEqual(response.status_code, 200)

    def test_upemail(self):
        data = {
            "type": "upemail",
            "fired_at": "2009-03-26 22:15:09",
            "data[list_id]": self.list.list_id,
            "data[new_id]": "51da8c3259",
            "data[new_email]": "api+new@mailchimp.com",
            "data[old_email]": "api+old@mailchimp.com"
        }
        response = self._mailchimp_webhook(data)
        self.assertEqual(response.status_code, 200)

    def test_profile(self):
        data = {
            "type": "profile",
            "fired_at": "2009-03-26 21:31:21",
            "data[id]": "8a25ff1d98",
            "data[list_id]": self.list.list_id,
            "data[email]": "api@mailchimp.com",
            "data[email_type]": "html",
            "data[merges][EMAIL]": "api@mailchimp.com",
            "data[merges][FNAME]": "MailChimp",
            "data[merges][LNAME]": "API",
            "data[merges][INTERESTS]": "Group1,Group2",
            "data[ip_opt]": "10.20.10.30"
        }
        response = self._mailchimp_webhook(data)
        self.assertEqual(response.status_code, 200)

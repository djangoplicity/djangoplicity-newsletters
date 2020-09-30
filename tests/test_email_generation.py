from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.urls import reverse
from datetime import datetime, timedelta

from djangoplicity.newsletters.models import NewsletterType, Newsletter, MailerParameter, Mailer


def create_mailer_parameter(mailer=None, name='', value='', type='str', help_text=None):
    return MailerParameter.objects.create(mailer=mailer, name=name, value=value, type=type, help_text=help_text)


def create_mailer(plugin, name):
    return Mailer.objects.create(plugin=plugin, name=name)


class TestEmailGeneration(TestCase):
    # LIST_NAME = 'esoepo-monitoring'
    # LIST_PASSWORD = 'ohsiechu'
    # LIST_BASEURL = 'http://www.eso.org/lists'

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@hubble.org',
            password='password123'
        )
        self.client.force_login(self.admin_user)

    @classmethod
    def setUpTestData(cls):
        Mailer.objects.all().delete()
        MailerParameter.objects.all().delete()
        Newsletter.objects.all().delete()
        NewsletterType.objects.all().delete()
        cls.mailer = create_mailer(
            plugin='djangoplicity.newsletters.mailers.MailChimpMailerPlugin',
            name='Newsletters news list'
        )
        # cls.mailer_parameters = [
        #     create_mailer_parameter(
        #         mailer=cls.mailer,
        #         name='enable_browser_link',
        #         value=True,
        #         type='bool',
        #         help_text="Enable 'view in browser' link"
        #     ),
        #     create_mailer_parameter(
        #         mailer=cls.mailer,
        #         name='list_id',
        #         value='ed25775a52',
        #         type='str',
        #         help_text='MailChimp list id - must be defined in djangoplicity.'
        #     )
        # ]
        cls.newsletter_type = NewsletterType.objects.create(
            name="ESA/Hubble News",
            slug="hubblenews",
            default_from_name="ESA/Hubble Information Centre",
            default_from_email="hubble@eso.org",
            subject_template="ESA/Hubble",
            text_template="*******************************************",
            html_template="""
            {% extends "newsletters/base.html" %}
            {% block header %}
                {% with width="700" height="280" color="#000000" logo_width="140" logo_url=base_url|add:MEDIA_URL|add:"esa_nl_logo.png" %}
                {% block header_content %}
                {% if data.release %}
                    {% with text_color="#ffffff" header_title="ESA/Hubble News" header_subtitle=data.release.release_date|date %}
                    {% with release_date=data.release.release_date link_url=base_url|add:data.release.get_absolute_url pretitle="ESA/Hubble "|add:data.release.release_type.name|add:" "|add:data.release.id embargo="" title=data.release.title subtitle=data.release.subtitle main_image=data.release.main_image %}
                    {% include "newsletters/includes/header.html" %}
                    {% endwith %}
                    {% endwith %}
                {% else %}
                    {% with text_color="#ffffff" header_title="ESA/Hubble News" header_subtitle="" %}
                    {% include "newsletters/includes/header.html" %}
                    {% endwith %}
                {% endif %}
            {% endblock %}
                {% endwith %}
            {% endblock %}""",
            archive=True,
            local_archive=False,
            internal_archive=False,
            sharing=False,
            subscribe_text="""<p style="text-align:right; padding-right: 20px">
                <a href="https://www.spacetelescope.org/subscribe/">Click here</a> to subscribe.
            </p>""",
        )
        cls.newsletter_type.mailers.add(cls.mailer)
        cls.newsletter = Newsletter.objects.create(
            type=cls.newsletter_type, frozen=False,
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(minutes=5),
            from_name='ESA/Hubble Information Centre',
            from_email='hubble@eso.org',
            subject='ESA/Hubble Science Release',
            text='',
            html='',
            editorial_subject='',
            editorial="""<p>Editorial</p>""",
            editorial_text="""
            For Your Information:
            ESA/Hubble Science Release 
            ---
            European Southern Observatory
            Email: hubble@eso.org"""
        )

    def test_newsletter_detail_html(self):
        """Test newsletter html is properly rendered"""
        url = '/newsletters/%s/html/%s' % (self.newsletter_type.slug, self.newsletter.pk)
        res = self.client.get(url, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.newsletter.editorial_subject)

    def test_newsletter_embed_html(self):
        """Test newsletter embed html is properly rendered"""
        url = '/newsletters/%s/htmlembed/%s' % (self.newsletter_type.slug, self.newsletter.pk)
        res = self.client.get(url, follow=True)

        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.newsletter.editorial_subject)

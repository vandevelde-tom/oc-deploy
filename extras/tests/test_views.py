import urllib.parse
import uuid

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from taggit.models import Tag

from dcim.models import Site
from extras.models import ConfigContext, ObjectChange


class TagTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        Tag.objects.bulk_create([
            Tag(name='Tag 1', slug='tag-1'),
            Tag(name='Tag 2', slug='tag-2'),
            Tag(name='Tag 3', slug='tag-3'),
        ])

    def test_tag_list(self):

        url = reverse('extras:tag_list')
        params = {
            "q": "tag",
        }

        response = self.client.get('{}?{}'.format(url, urllib.parse.urlencode(params)))
        self.assertEqual(response.status_code, 200)


class ConfigContextTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        site = Site(name='Site 1', slug='site-1')
        site.save()

        # Create three ConfigContexts
        for i in range(1, 4):
            configcontext = ConfigContext(
                name='Config Context {}'.format(i),
                data='{{"foo": {}}}'.format(i)
            )
            configcontext.save()
            configcontext.sites.add(site)

    def test_configcontext_list(self):

        url = reverse('extras:configcontext_list')
        params = {
            "q": "foo",
        }

        response = self.client.get('{}?{}'.format(url, urllib.parse.urlencode(params)))
        self.assertEqual(response.status_code, 200)

    def test_configcontext(self):

        configcontext = ConfigContext.objects.first()
        response = self.client.get(configcontext.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class ObjectChangeTestCase(TestCase):

    def setUp(self):

        self.client = Client()

        user = User(username='testuser', email='testuser@example.com')
        user.save()

        site = Site(name='Site 1', slug='site-1')
        site.save()

        # Create three ObjectChanges
        for i in range(1, 4):
            site.log_change(
                user=user,
                request_id=uuid.uuid4(),
                action=2
            )

    def test_objectchange_list(self):

        url = reverse('extras:objectchange_list')
        params = {
            "user": User.objects.first(),
        }

        response = self.client.get('{}?{}'.format(url, urllib.parse.urlencode(params)))
        self.assertEqual(response.status_code, 200)

    def test_objectchange(self):

        objectchange = ObjectChange.objects.first()
        response = self.client.get(objectchange.get_absolute_url())
        self.assertEqual(response.status_code, 200)

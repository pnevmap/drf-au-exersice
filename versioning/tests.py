import os
import time

from django.core.files import File
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
import mock
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.utils import json

from versioning.models import Document, Revision


def tearDownModule():
    from base import settings
    full_path = os.path.join(settings.BASE_DIR, 'users\\temporary\\')
    for path, directories, files in os.walk(full_path):
        for f in files:
            os.remove(os.path.join(full_path, f))


class RevisionModelTests(TestCase):
    """
    tests for the Revision model
    """
    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def tearDown(self):
        pass

    def test_revision_index_and_revision_url(self):
        document = Document.objects.create(url='some-url', owner=User.objects.get(username='temporary'))
        revision0 = Revision.objects.create(document=document)
        revision1 = Revision.objects.create(document=document)
        revision2 = Revision.objects.create(document=document)

        self.assertEqual(revision0.index, 0)
        self.assertEqual(revision1.index, 1)
        self.assertEqual(revision2.index, 2)

        self.assertEqual(revision0.revision_url, "some-url?revision=0")
        self.assertEqual(revision1.revision_url, "some-url?revision=1")
        self.assertEqual(revision2.revision_url, "some-url?revision=2")

    def test_revision_revision_assert_fields(self):
        mock_file = mock.MagicMock(spec=File)
        mock_file.name = 'test-file.jpg'
        user = User.objects.get(username='temporary')
        document = Document.objects.create(url='some/url', owner=user)
        revision = Revision.objects.create(document=document, file=mock_file)
        self.assertEqual(revision.url, "users/temporary/test-file.0.jpg")
        self.assertEqual(revision.revision_url, "some/url?revision=0")
        self.assertEqual(revision.document_url, "some/url")
        self.assertEqual(revision.document_owner, user)

    def test_upload_to(self):
        pass


def create_test_file(file_name='users/temporary/yet-test-file.txt', content="here is some content!"):
    f = open(file_name, "x")
    f.write(content)
    f.close()


class DocumentAPITests(APITestCase):
    """
    tests the Document API
    """
    user = User

    def setUp(self):
        get_user_model().objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.user = User.objects.get(username='temporary')

    def tearDown(self):
        self.client.logout()
        pass

    def test_create_document_when_not_logged_in_401(self):
        url = '/documents/'
        data = {'url': 'some/url/file.ext'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_document_assert_fields(self):
        self.client.login(username='temporary', password='temporary')
        test_file_name = "users/temporary/post.txt"
        test_document_url = 'post/url/post.txt'
        create_test_file(test_file_name)
        data = {'url': test_document_url, 'file': open(test_file_name)}

        response = self.client.post('/documents/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        document = Document.objects.filter(url=test_document_url).get()
        self.assertEqual(document.url, test_document_url)
        self.assertEqual(document.revisions.count(), 1)
        self.assertEqual(document.revisions.first().file.name, 'users/temporary/post.0.txt')
        self.assertEqual(document.owner, self.user)

        self.client.logout()

    def test_create_document_on_existing_url_returns_500(self):
        self.client.login(username='temporary', password='temporary')
        test_file_name1 = "users/temporary/post500-1.txt"
        test_document_url = 'post/url/post500.txt'
        create_test_file(test_file_name1)
        data = {'url': test_document_url, 'file': open(test_file_name1)}
        response = self.client.post('/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_file_name2 = "users/temporary/post500-2.txt"

        create_test_file(test_file_name2)

        self.client.raise_request_exception = False
        data = {'url': test_document_url, }
        response = self.client.post('/documents/', data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

        self.client.logout()

    def test_add_new_revision_assert_fields(self):
        self.client.login(username='temporary', password='temporary')

        test_file_name = "users/temporary/put.txt"
        test_file_name_revision_1 = "users/temporary/put-revision-1.txt"
        test_document_url = 'put/url/put.txt'
        create_test_file(test_file_name)
        data = {'url': test_document_url, 'file': open(test_file_name)}
        response = self.client.post('/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        create_test_file(test_file_name_revision_1)
        response = self.client.put(f'/documents/{test_document_url}/', {'file': open(test_file_name_revision_1)}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        document = Document.objects.filter(url=test_document_url).get()
        self.assertEqual(document.revisions.count(), 2)
        self.assertEqual(document.revisions.last().revision_url, 'put/url/put.txt?revision=1')
        self.assertEqual(document.revisions.last().file.name, 'users/temporary/put-revision-1.1.txt')
        self.assertEqual(document.owner, self.user)

        self.client.logout()

    def test_list_document_assert_fields(self):
        self.client.login(username='temporary', password='temporary')

        test_file_name = "users/temporary/get.txt"
        test_file_name_revision_1 = "users/temporary/get-revision-1.txt"
        test_document_url = 'get/url/get.txt'
        create_test_file(test_file_name)
        data = {'url': test_document_url, 'file': open(test_file_name)}
        response = self.client.post('/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        create_test_file(test_file_name_revision_1)
        response = self.client.put(f'/documents/{test_document_url}/', {'file': open(test_file_name_revision_1)}, format= 'multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        documents = json.loads(response.content)
        self.assertEqual(documents[0]['url'], test_document_url)
        self.assertEqual(documents[0]['revisions'][0],  'get/url/get.txt?revision=0')
        self.assertEqual(documents[0]['revisions'][1], 'get/url/get.txt?revision=1')
        self.client.logout()

    def test_list_only_owned_documents(self):
        get_user_model().objects.create_user('other-user', 'temporary@gmail.com', 'other-user')
        self.client.login(username='temporary', password='temporary')

        Document.objects.create(url='some-url', owner=User.objects.get(username='temporary'))
        Document.objects.create(url='some-other-url', owner=User.objects.get(username='other-user'))
        response = self.client.get('/documents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        documents = response.data
        self.assertEqual(len(documents), 1)
        self.client.logout()

    def test_retrieve_200_assert_fields(self):
        self.client.login(username='temporary', password='temporary')

        test_file_name = "users/temporary/retrieve.txt"
        test_document_url = 'url/retrieve.txt'
        create_test_file(test_file_name)
        data = {'url': test_document_url, 'file': open(test_file_name)}
        response = self.client.post('/documents/', data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get('/documents/url/retrieve.txt/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # todo
        # assert file response is equal to the posted file
        self.client.logout()

    def test_retrieve_unauthorized_401(self):
        get_user_model().objects.create_user('unauthorized', 'temporary@gmail.com', 'unauthorized')
        self.client.login(username='unauthorized', password='unauthorized')

        Document.objects.create(url='some-url', owner=User.objects.get(username='temporary'))
        response = self.client.get('/documents/some-url/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.logout()

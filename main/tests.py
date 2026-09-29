from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from .models import Task


User = get_user_model()


class TaskAccessTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='alice', password='test-pass-123')
		self.other_user = User.objects.create_user(username='bob', password='test-pass-123')

	def test_index_only_shows_tasks_owned_by_current_user(self):
		Task.objects.create(user=self.user, name='Alice task')
		Task.objects.create(user=self.other_user, name='Bob task')
		Task.objects.create(user=None, name='Legacy task')
		self.client.force_login(self.user)

		response = self.client.get('/')

		self.assertContains(response, 'Alice task')
		self.assertNotContains(response, 'Bob task')
		self.assertNotContains(response, 'Legacy task')

	def test_create_task_assigns_current_user(self):
		self.client.force_login(self.user)

		response = self.client.post('/create_task/', {
			'name': 'New task',
			'description': '',
			'project': 'studies',
			'priority': 'short',
			'date': '',
		})

		self.assertEqual(response.status_code, 302)
		task = Task.objects.get(name='New task')
		self.assertEqual(task.user, self.user)

	def test_api_requires_authentication(self):
		response = self.client.get('/api/Task/')

		self.assertEqual(response.status_code, 403)

	def test_api_only_lists_current_users_tasks(self):
		Task.objects.create(user=self.user, name='Alice task')
		Task.objects.create(user=self.other_user, name='Bob task')
		self.client.force_login(self.user)

		response = self.client.get('/api/Task/')

		self.assertEqual(response.status_code, 200)
		self.assertEqual([task['name'] for task in response.json()], ['Alice task'])

	def test_api_creation_uses_authenticated_user(self):
		api_client = APIClient()
		api_client.force_authenticate(user=self.user)

		response = api_client.post('/api/Task/', {
			'name': 'API task',
			'project': 'personal',
			'priority': 'high',
			'user': self.other_user.pk,
		}, format='json')

		self.assertEqual(response.status_code, 201)
		task = Task.objects.get(name='API task')
		self.assertEqual(task.user, self.user)

	def test_login_required_redirects_to_local_login_page(self):
		response = self.client.get('/')

		self.assertRedirects(response, '/accounts/login/?next=/')

	@override_settings(SOCIALACCOUNT_PROVIDERS={
		'google': {'SCOPE': ['profile', 'email'], 'AUTH_PARAMS': {'prompt': 'select_account'}}
	})
	def test_login_page_hides_google_button_without_credentials(self):
		response = self.client.get('/accounts/login/')

		self.assertEqual(response.status_code, 200)
		self.assertNotContains(response, '/accounts/google/login/')

	@override_settings(SOCIALACCOUNT_PROVIDERS={
		'google': {
			'SCOPE': ['profile', 'email'],
			'AUTH_PARAMS': {'prompt': 'select_account'},
			'APP': {'client_id': 'test-client-id', 'secret': 'test-client-secret', 'key': ''},
		}
	})
	def test_google_oauth_redirects_when_credentials_are_configured(self):
		response = self.client.get('/accounts/login/')
		self.assertContains(response, '/accounts/google/login/')

		response = self.client.post('/accounts/google/login/')

		self.assertEqual(response.status_code, 302)
		self.assertIn('accounts.google.com', response['Location'])

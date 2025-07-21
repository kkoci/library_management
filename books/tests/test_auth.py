from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

class JWTAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='jwtuser',
            email='jwt@example.com',
            password='jwtpass123'
        )

    def test_jwt_token_obtain_and_access_protected_view(self):
        # Obtain token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': self.user.username,
            'password': 'jwtpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        token = response.data['access']

        # Use token to access protected endpoint (e.g., book list)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(reverse('book-list-create'))
        self.assertEqual(response.status_code, 200)

    def test_access_protected_view_without_token(self):
        response = self.client.get(reverse('book-list-create'))
        # Since permission is IsAdminOrReadOnly, unauthenticated GET returns 200 OK
        self.assertEqual(response.status_code, 200)

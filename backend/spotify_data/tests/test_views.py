"""Unit tests for spotify_data/views (adding and updating users)."""

from unittest.mock import patch
import json
import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from spotify_data.views import update_or_add_spotify_user
from accounts.models import SpotifyToken


@pytest.fixture
def user():
    """Fixture to create a user instance."""
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def mock_request(mocker):
    """Fixture to mock the request object."""
    mock = mocker.Mock()
    mock.user = mocker.Mock()  # Mock user object
    return mock


@pytest.fixture
def session_id():
    """Instantiates test session id."""
    return "test_session_id"


@pytest.fixture
def mock_token():
    """Instantiates test access token."""
    return {
        'access_token': 'test_access_token',
        'expires_in': timezone.now() + timezone.timedelta(seconds=3600),  # 1 hour
        'refresh_token': 'test_refresh_token',
        'token_type': 'Bearer'
    }


@pytest.fixture
def mock_user_data():
    """Instantiates test user data."""
    return {
        'id': 'spotify_user_id',
        'display_name': 'Test User',
        'email': 'testuser@example.com',
        'images': [{'url': 'http://example.com/image.jpg'}]
    }

@pytest.mark.django_db
def test_user_not_authenticated(mock_request, session_id):
    """Test when user is not authenticated."""
    with patch('accounts.views.is_spotify_authenticated', return_value=False):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 403
        assert json.loads(response.content) == {'error': 'User not authenticated'}


@pytest.mark.django_db
def test_missing_access_token(mock_request, session_id, user):
    """Test when access token does not exist."""

    mock_request.user = user

    # Patch the is_spotify_authenticated function
    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', side_effect=ObjectDoesNotExist):
        response = update_or_add_spotify_user(mock_request, session_id)

        assert response.status_code == 403  # Adjusted to match the expected behavior
        assert json.loads(response.content) == {'error': 'User not authenticated'}


@pytest.mark.django_db
def test_successful_user_update(mock_request, session_id, mock_token, mock_user_data, user):
    """Test successful user update when the user already exists."""
    mock_request.user = user

    # Create the token with a valid datetime for expires_in
    token_entry = SpotifyToken.objects.create(
        user=session_id,
        access_token=mock_token['access_token'],
        expires_in=timezone.now() + timezone.timedelta(seconds=3600)  # 1 hour from now
    )

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=mock_user_data):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 200
        assert 'spotify_user' in json.loads(response.content)

@pytest.mark.django_db
def test_failed_user_data_fetch(mock_request, session_id, mock_token):
    """Test when fetching user data from Spotify fails."""
    token_entry = SpotifyToken(user=session_id, access_token=mock_token['access_token'],
                               expires_in=timezone.now() + timezone.timedelta(seconds=3600))
    SpotifyToken.objects.create(user=session_id, **mock_token)

    with patch('accounts.views.is_spotify_authenticated', return_value=True), \
            patch('accounts.models.SpotifyToken.objects.get', return_value=token_entry), \
            patch('spotify_data.views.get_spotify_user_data', return_value=None):
        response = update_or_add_spotify_user(mock_request, session_id)
        assert response.status_code == 500
        assert json.loads(response.content) == {'error': 'Could not fetch user data from Spotify'}
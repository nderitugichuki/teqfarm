import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="manager",
        email="manager@teqfarm.test",
        password="StrongPass!2468",
        first_name="Farm",
        last_name="Manager",
        role=User.Role.MANAGER,
    )


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def authenticated_client(client, user):
    client.force_authenticate(user=user)
    return client


@pytest.mark.django_db
def test_login_returns_tokens_and_user(client, user):
    response = client.post(
        reverse("accounts:login"),
        {"username": user.username, "password": "StrongPass!2468"},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["access"]
    assert response.data["refresh"]
    assert response.data["user"]["role"] == User.Role.MANAGER


@pytest.mark.django_db
def test_profile_requires_authentication(client):
    response = client.get(reverse("accounts:profile"))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data["success"] is False


@pytest.mark.django_db
def test_user_can_update_own_profile(authenticated_client, user):
    response = authenticated_client.patch(
        reverse("accounts:profile"), {"phone_number": "+254700000000"}
    )
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.phone_number == "+254700000000"


@pytest.mark.django_db
def test_change_password_validates_current_password(authenticated_client):
    response = authenticated_client.post(
        reverse("accounts:change-password"),
        {
            "current_password": "wrong-password",
            "new_password": "NewStrongPass!8642",
            "confirm_password": "NewStrongPass!8642",
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "current_password" in response.data["errors"]


@pytest.mark.django_db
def test_change_password_updates_credentials(authenticated_client, user):
    response = authenticated_client.post(
        reverse("accounts:change-password"),
        {
            "current_password": "StrongPass!2468",
            "new_password": "NewStrongPass!8642",
            "confirm_password": "NewStrongPass!8642",
        },
    )
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password("NewStrongPass!8642")


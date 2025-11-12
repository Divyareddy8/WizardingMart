import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from base.models import Product, Cart


# ---------------------------
# FIXTURES
# ---------------------------

@pytest.fixture
def client(db, client):
    return client


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser",
        password="testpass123"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(
        username="admin",
        password="adminpass",
        email="admin@test.com"
    )


@pytest.fixture
def product(db):
    return Product.objects.create(
        name="Magic Wand",
        description="Test product",
        mrp=100,
        price=80,
        productImg="https://example.com/image.png"
    )


# ---------------------------
# UNIT TESTING
# ---------------------------

@pytest.mark.django_db
def test_home_page_loads(client):
    response = client.get("/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_movies_page_loads(client):
    response = client.get("/movies/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_page_get(client):
    response = client.get("/login/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_success(client, user):
    response = client.post("/login/", {
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 302   # redirect on success


@pytest.mark.django_db
def test_login_failure(client):
    response = client.post("/login/", {
        "username": "wrong",
        "password": "wrong"
    })
    assert response.status_code == 200   # stays on page


# ---------------------------
# MODULE TESTING
# ---------------------------

@pytest.mark.django_db
def test_shop_page(client, product):
    response = client.get("/shop/")
    assert response.status_code == 200
    assert "Magic Wand" in response.content.decode()


@pytest.mark.django_db
def test_cart_requires_login(client):
    response = client.get("/cart/")
    assert response.status_code == 302   # redirect to login


@pytest.mark.django_db
def test_admin_login(admin_user, client):
    response = client.post("/admin/login/", {
        "username": "admin",
        "password": "adminpass"
    })
    assert response.status_code in [200, 302]


# ---------------------------
# INTEGRATION TESTING
# ---------------------------

@pytest.mark.django_db
def test_add_item_to_cart_flow(client, user, product):
    # login first
    client.login(username="testuser", password="testpass123")

    # add item
    response = client.post(f"/add_item/{product.id}/")
    assert response.status_code == 200

    data = response.json()
    assert data["total_quantity"] == 1


@pytest.mark.django_db
def test_cart_view_after_add(client, user, product):
    client.login(username="testuser", password="testpass123")
    client.post(f"/add_item/{product.id}/")

    response = client.get("/cart/")
    assert response.status_code == 200
    assert "Magic Wand" in response.content.decode()


@pytest.mark.django_db
def test_delete_item_from_cart(client, user, product):
    client.login(username="testuser", password="testpass123")

    client.post(f"/add_item/{product.id}/")
    cart_item = Cart.objects.get(customer=user)

    response = client.post(f"/delete_item/{cart_item.id}/")
    assert response.status_code == 200

    data = response.json()
    assert "removed" in data["message"]


@pytest.mark.django_db
def test_checkout_page(client, user, product):
    client.login(username="testuser", password="testpass123")
    client.post(f"/add_item/{product.id}/")

    response = client.get("/checkout/")
    assert response.status_code == 200


# ---------------------------
# LOGOUT TEST
# ---------------------------

@pytest.mark.django_db
def test_logout(client, user):
    client.login(username="testuser", password="testpass123")
    response = client.get("/logout/")
    assert response.status_code == 302

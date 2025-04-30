import stripe
from django.contrib.auth import get_user_model

from config.settings import SECRET_STRIPE_KEY
from materials.models import Lesson

stripe.api_key = SECRET_STRIPE_KEY


def create_product(product):
    """Create product in Stripe."""
    lesson_name = Lesson.objects.get(id=product).name # getting Lesson name
    course_name = Lesson.objects.get(id=product).course # getting Course name
    product_name = f"Course: {course_name}\nLesson: {lesson_name}"
    return stripe.Product.create(name=product_name)


def create_price(amount, product):
    """Create price in Stripe."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=amount * 100,
        product_data={"name": product},
    )

    return price


def create_session(price):
    """Create session in Stripe."""

    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def create_user():
    User = get_user_model()
    for user in range(1, 6):
        user = User.objects.create(
            email=f"user{user}@user.com",
        )

        user.set_password("1234")
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        user.save()

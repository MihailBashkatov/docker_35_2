from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """Registering model User"""

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="City")
    phone_number = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="Phone number"
    )
    avatar = models.ImageField(
        upload_to="users/images/%Y/%m/%d/",
        default=None,
        null=True,
        blank=True,
        verbose_name="Saved user image",
    )
    last_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = [
            "email",
        ]

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Registering model Payment"""

    CASH = "Cash"
    CARD = "Card"

    STATUS_CHOICES = [
        (CASH, "Cash"),
        (CARD, "Card"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )

    payment_date = models.DateField(auto_now=True, verbose_name="Payment date")

    payment_summ = models.FloatField(verbose_name="Payment Summ")

    payment_mode = models.CharField(
        max_length=4,
        choices=STATUS_CHOICES,
        default=CARD,
        verbose_name="Payment mode",
    )

    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paid_course",
    )

    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="paid_lesson",
    )

    session_id = models.CharField(max_length=400, blank=True, null=True, verbose_name='Link to the session')

    link = models.URLField(max_length=400, blank=True, null=True, verbose_name='Link to the session')

    def __str__(self):

        if self.paid_course and self.paid_lesson:
            return f"Course: {self.paid_course}, lesson: {self.paid_lesson}"
        elif self.paid_course:
            return self.paid_course
        else:
            return self.paid_lesson

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

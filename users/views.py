from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from materials.models import Lesson
from users.models import Payment, User
from users.serializers import (PaymentSerializer, UserPaymentsSerializer,
                               UserSerializer)
from users.utils import create_price, create_product, create_session


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetreiveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    search_fields = ("payment_mode", "paid_course", "paid_lesson")
    ordering_fields = ("payment_date",)


class UserPaymentsListAPIView(generics.ListAPIView):
    serializer_class = UserPaymentsSerializer
    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):

        payment = serializer.save(user=self.request.user)

        product = create_product(
            self.request.data["paid_lesson"]
        )  # Creating lesson for payment
        price = create_price(
            self.request.data["payment_summ"], product.name
        )  # Creating price for the lesson
        session_id, payment_link = create_session(
            price
        )  # Creating session for the payment
        paid_course = Lesson.objects.get(
            id=self.request.data["paid_lesson"]
        ).course  # Identifying course for the lesson

        payment.paid_course = paid_course
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

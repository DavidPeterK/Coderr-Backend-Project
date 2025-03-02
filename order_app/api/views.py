from rest_framework.views import APIView
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from order_app.models import Order
from order_app.api.serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer_user=self.request.user)

    def perform_create(self, serializer):
        offer_detail = serializer.validated_data['offer_detail']
        serializer.save(
            customer_user=self.request.user,
            business_user=offer_detail.offer.user
        )


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        order_count = Order.objects.filter(
            business_user_id=business_user_id, status='in_progress').count()
        return Response({'order_count': order_count}, status=status.HTTP_200_OK)


class CompletedOrderCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, business_user_id):
        completed_order_count = Order.objects.filter(
            business_user_id=business_user_id, status='completed').count()
        return Response({'completed_order_count': completed_order_count}, status=status.HTTP_200_OK)

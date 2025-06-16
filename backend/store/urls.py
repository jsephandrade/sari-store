from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterView

from .views import (
    ProductViewSet,
    CustomerViewSet,
    UtangEntryViewSet,
    PaymentViewSet,
    SummaryViewSet,
    CategoryViewSet,
    PriceAdjustmentViewSet,
    SaleViewSet,
)

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'utang', UtangEntryViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'price-adjustments', PriceAdjustmentViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'summary', SummaryViewSet, basename='summary')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]

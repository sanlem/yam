from rest_framework.routers import DefaultRouter
from .views import MessageViewSet


router = DefaultRouter()
router.register(r'', MessageViewSet, base_name="message")

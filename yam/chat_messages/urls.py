from rest_framework.routers import DefaultRouter
from .views import MessageViewSet


router = DefaultRouter()
router.register(r'messages', MessageViewSet, base_name="message")
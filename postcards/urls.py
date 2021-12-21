from rest_framework.routers import DefaultRouter

from postcards.views import PostcardCreatorCredentialsViewSet

router = DefaultRouter()
router.register(r'credentials', PostcardCreatorCredentialsViewSet, basename='credentials')

urlpatterns = router.urls
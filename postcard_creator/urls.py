from rest_framework.routers import DefaultRouter

from postcard_creator.views import PostcardCreatorCredentialsViewSet

router = DefaultRouter()
router.register(r'', PostcardCreatorCredentialsViewSet, basename='credentials')

urlpatterns = router.urls
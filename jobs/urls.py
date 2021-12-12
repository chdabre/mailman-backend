from rest_framework.routers import DefaultRouter

from .views import PostcardJobViewset

router = DefaultRouter()
router.register(r'', PostcardJobViewset, basename='jobs')

urlpatterns = router.urls
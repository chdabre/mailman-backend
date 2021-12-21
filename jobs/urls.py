from rest_framework.routers import DefaultRouter

from .views import PostcardJobViewset, AddressViewset

router = DefaultRouter()
router.register(r'jobs', PostcardJobViewset, basename='jobs')
router.register(r'address', AddressViewset, basename='addresses')

urlpatterns = router.urls
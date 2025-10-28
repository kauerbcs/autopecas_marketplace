from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PartViewSet


router = DefaultRouter()
router.register('parts', PartViewSet, basename='part')


urlpatterns = [
	path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers
from .views import (
    DeathStatisticViewSet, 
    PreventStatisticViewSet,
    DiseaseGroupViewSet,
    RegionViewSet
)

router = routers.DefaultRouter()
router.register(r'disease-groups', DiseaseGroupViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'death-statistics', DeathStatisticViewSet, basename = 'death-statistics')
router.register(r'prevent-statistics', PreventStatisticViewSet, basename = 'prevent-statistics')

urlpatterns = [
    path('', include(router.urls)),
]
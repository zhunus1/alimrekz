from django.urls import path, include
from rest_framework import routers
from .views import DeathStatisticViewSet, PreventStatisticViewSet

router = routers.DefaultRouter()
router.register(r'death-statistics', DeathStatisticViewSet)
router.register(r'prevent-statistics', PreventStatisticViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
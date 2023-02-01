from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tables', views.BookingViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.MenuListView.as_view(), name='menu-list'),
    path('menu/<int:pk>', views.MenuDetailView.as_view(), name='menu-detail'),
]

urlpatterns += router.urls
from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name="about"),
    path('menu', views.menu_list, name="menu-list"),
    path('menu/<int:pk>', views.menu_detail, name="menu-detail"),
    path('reservations', views.reservations, name="reservations"),
    path('book', views.book, name="book"),
    # api
    path('api/menu', views.MenuListView.as_view(), name='api-menu-list'),
    path('api/menu/<int:pk>', views.MenuDetailView.as_view(), name='api-menu-detail'),
]

urlpatterns += router.urls
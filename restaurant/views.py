import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .forms import BookingForm
from .serializers import (
    MenuSerializer,
    BookingSerializer
)
from .models import (
    Menu,
    Booking
)

# Create your views here.


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def menu_list(request):
    menus = Menu.objects.all()
    return render(request, 'menu.html', {'menu': menus})


def menu_detail(request, pk):
    menuitem = get_object_or_404(Menu, pk=pk)
    return render(request, 'menu_item.html', {'menu_item': menuitem})


def reservations(request):
    bookings = Booking.objects.all()
    bookings_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html', {'bookings': bookings_json})


def book(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'book.html', {'form': BookingForm()})


def bookings(request):
    if request.method == 'POST':
        data = json.loads(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if not exist:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot']
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)
    bookings_json = BookingSerializer(bookings, many=True)
    return HttpResponse(bookings_json.data, content_type='application/json')


class MenuListView(generics.ListCreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Booking.objects.all()
        date = self.request.query_params.get('date')
        if date is not None:
            queryset = queryset.filter(reservation_date=date)
        return queryset
    

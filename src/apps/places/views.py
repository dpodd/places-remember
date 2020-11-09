from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .models import Memory
from .forms import MemoryModelForm
from geopy.geocoders import Nominatim
import folium

geolocator = Nominatim(user_agent='places')


def profile(request, *args, **kwargs):
    queryset = Memory.objects.filter(user_id=request.user.id)
    form = MemoryModelForm(request.POST or None)

    # placeholder address, for dev
    location = geolocator.geocode('Krasnoyarsk')
    lat_0 = location.latitude
    long_0 = location.longitude
    pointA = (lat_0, long_0)

    # map
    m = folium.Map(width=800, height=500, location=pointA)
    m = m._repr_html_()

    if form.is_valid():
        instance = form.save(commit=False)
        instance.title = form.cleaned_data.get('title')
        instance.user = request.user
        instance.description = form.cleaned_data.get('description')
        instance.location = lat_0, long_0
        instance.save()

    context = {
        "message" : "Context has passed.",
        "memories" : queryset,
        "form" : form,
        "map" : m,
    }
    return render(request, 'home.html', context)


class HomePageView(TemplateView):
    template_name = "home.html"

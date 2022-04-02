from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, JsonResponse
from .models import coords
import requests
from rest_framework.authtoken.models import Token
from .models import registeredWebsite

def index(request):
    return render(request, 'index.html')

def mapperRedirect(request, username_val):
    if username_val == request.user.username:
        if registeredWebsite.objects.filter(username = username_val).exists():
            registered_website_json = list(registeredWebsite.objects.filter(username = username_val).values())
            return redirect(f"/mapper/{username_val}/{registered_website_json[0]['id']}")
        else:
            return redirect('/accounts/profile')


def mapper(request, username_val, site_id):
    if username_val == request.user.username:
        coords_data_json = list(coords.objects.filter(username = request.user.username, website_id = site_id).values())
        return render(request, 'map.html', {'coords_data_json': coords_data_json, 'site_id_context': site_id})
    else:
        return HttpResponse('Login to access this page')


def storeData(request, username_slug, access_token, site_id, lat_slug, long_slug, ip_address_slug):
    token = Token.objects.get(user = request.user.pk)
    if access_token == str(token):
        if User.objects.filter(username=username_slug).exists():
            url = f'https://api.geoapify.com/v1/geocode/reverse?lat={lat_slug}&lon={long_slug}&apiKey=73d3c2b4c96c4a7495198a3981b102cf'
            response = requests.get(url)
            data = response.json()
            city = ''
            state = ''
            country = ''
            if 'city' in data['features'][0]['properties']:
                city = data['features'][0]['properties']['city']
            if 'state' in data['features'][0]['properties']:
                state = data['features'][0]['properties']['state']
            if 'country' in data['features'][0]['properties']:
                country = data['features'][0]['properties']['country']

            if not coords.objects.filter(username = username_slug, website_id = site_id, ip_address = ip_address_slug).exists():
                coords.objects.create(username = username_slug, access_token = access_token, website_id = site_id, lat = lat_slug, long = long_slug, city = city, state = state, country = country, ip_address = ip_address_slug)
                data_json = {
                'status': 'success'
                }
                return JsonResponse(data_json, safe = False)
        err_data_json = {
        'status': 'failedd'
        }
        return JsonResponse(err_data_json, safe = False)


def coordsDataJson(request, site_id):
    coords_data_json = list(coords.objects.filter(username = request.user.username, website_id = site_id).values())
    return JsonResponse(coords_data_json, safe = False)


def registeredSiteDataJson(request):
    data_json = list(registeredWebsite.objects.filter(username = request.user.username).values())
    return JsonResponse(data_json, safe = False)

def integration(request):
    userRegisteredSites = list(registeredWebsite.objects.filter(username = request.user.username).values())
    registeredSiteId = userRegisteredSites[-1]['id']
    token = Token.objects.get(user = request.user.pk)
    return render(request, 'integration.html', {'token': token, 'registeredSiteId': registeredSiteId})

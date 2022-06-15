from django.shortcuts import render,redirect
from django.http import HttpResponseBadRequest, JsonResponse
from trip_data.models import Trip_data
from django.forms.models import model_to_dict

from django.http import HttpResponseRedirect
from django.urls import reverse


# Create your views here.
from django.http import HttpResponse

def main(request):
    return render(request, 'index.html')

def trip_data(request,num=0,keyword=None):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            if keyword=='null':
                trip_data = list(Trip_data.objects.all()[(num*12):((num+1)*12)].values())
            else:
                trip_data = list(Trip_data.objects.filter(stitle__contains = keyword)[(num*12):((num+1)*12)].values())
            if len(trip_data)==12:
                nextpage = num+1
            else:
                nextpage = None
            return JsonResponse({'data': trip_data,"nextpage": nextpage})
        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest({'error':True})


def attraction_web(request,num):
    return render(request, 'attraction.html')

def attraction(request,num):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax:
        if request.method == 'GET':
            try:
                trip_data = Trip_data.objects.get(pk=num)
                trip_data = model_to_dict(trip_data)
            except Trip_data.DoesNotExist:
                trip_data = None
            return JsonResponse({'data': trip_data,})

        return JsonResponse({'status': 'Invalid request'}, status=400)
    else:
        return HttpResponseBadRequest({'error':True})

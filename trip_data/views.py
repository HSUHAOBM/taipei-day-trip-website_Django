from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from trip_data.models import Trip_data

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
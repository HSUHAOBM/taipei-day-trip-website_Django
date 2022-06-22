from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from order.models import Order
from django.http import HttpResponseBadRequest, JsonResponse
from trip_data.models import Trip_data

import json
from order.use_taypay import paybyprime

# Create your views here.

def main(request):
    return render(request, 'booking.html')

@csrf_exempt
def book(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    # if request.is_ajax():
    if is_ajax:
        try:
            user_name = request.session.get('user_name')
            user_email = request.session.get('user_email')
        except:
            pass

        if request.method == 'GET':
            if user_name:
                order_data = request.session.get('order')
                print(order_data)
                if order_data:
                    return JsonResponse({'data': order_data,'mseeage' : '登入中'})
            else :
                return JsonResponse({"error" : True, 'message' : '錯誤',})

        if request.method == 'POST':
            if user_name:
                data = request.body.decode('utf-8')
                data = json.loads(data)
                trip_data = Trip_data.objects.get(pk=data['attractionId'])
                print(trip_data.stitle)
                order_time = data['time']
                order_date = data['date']
                order_price = data['price']

                request.session["order"] = {
                    'order_trip' : {
                        "id" : trip_data.id,
                        "name" : trip_data.stitle,
                        "category" : trip_data.category,
                        "description" : "，".join(trip_data.description.split("，")[:]),
                        "address" : trip_data.address,
                        "transport" : trip_data.transport,
                        "mrt" : trip_data.mrt,
                        "latitude" : trip_data.latitude,
                        "longitude": trip_data.longitude,
                        "images" : trip_data.images
                    },
                    'order_time' : order_time,
                    'order_date' : order_date,
                    'order_price' : order_price
                }
                return JsonResponse ({"ok" : True, "message" : "資料送出成功"})

            else:
                return JsonResponse({"error" : True, 'message' : "未登入",})


@csrf_exempt
def order(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    # if request.is_ajax():
    if is_ajax:
        try:
            user_name = request.session.get('user_name')
            user_email = request.session.get('user_email')
        except:
            pass

        if request.method == 'GET':
            if user_name:
                order_data = request.session.get('order')
                print(order_data)
                if order_data:
                    return JsonResponse({'data': order_data,'mseeage' : '登入中'})
            else :
                return JsonResponse({"error" : True, 'message' : '錯誤',})

        if request.method == 'POST':
            if user_name:
                data = request.body.decode('utf-8')
                data = json.loads(data)
                print(data)
                order_data = request.session.get('order')
                tappaypay_prime = paybyprime(data)
                if tappaypay_prime["status"] == 0:
                    print(tappaypay_prime)
                    print('訂單成立')
                return JsonResponse ({"ok" : True, "message" : "資料送出成功"})

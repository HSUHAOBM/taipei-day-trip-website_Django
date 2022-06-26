from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from order.models import Order
from django.http import HttpResponseBadRequest, JsonResponse
from trip_data.models import Trip_data
from member.models import Member
from django.forms.models import model_to_dict

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
            user_id = request.session.get('user_id')
        except:
            return JsonResponse({"error" : True, 'message' : "未登入",})

        if request.method == 'GET':
            if user_name:
                order_data = request.session.get('order')
                if order_data:
                    return JsonResponse({'data': order_data,'mseeage' : '登入中'})
                else:
                    return JsonResponse({'data': order_data,'mseeage' : '登入中'})

            else :
                return JsonResponse({"error" : True, 'message' : '錯誤',})

        if request.method == 'POST':
            if user_name:
                data = request.body.decode('utf-8')
                data = json.loads(data)
                trip_data = Trip_data.objects.get(pk=data['attractionId'])
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
                return JsonResponse ({"ok" : True, "message" : "資料送出成功",})

            else:
                return JsonResponse({"error" : True, 'message' : "未登入",})
        if request.method == 'DELETE':
            del request.session['order']
            return JsonResponse({"ok" : True, 'message' : '錯誤',})



@csrf_exempt
def order(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    # if request.is_ajax():
    if is_ajax:
        try:
            user_name = request.session.get('user_name')
            user_email = request.session.get('user_email')
            user_id = request.session.get('user_id')
        except:
            return JsonResponse({"error" : True, 'message' : "未登入",})

        if request.method == 'PATCH':
            if user_name:
                try:
                    data = request.body.decode('utf-8')
                    data = json.loads(data)
                    order_id = data['order_number']
                    order = Order.objects.get(pk=order_id)
                    if order.user_id.id != user_id:
                        return JsonResponse({'erorr': True,'mseeage' : '只能看到自己的訂單'})
                    trip_data = Trip_data.objects.get(pk=order.trip_id.id)
                    trip_data = model_to_dict(trip_data)
                    order = model_to_dict(order)
                except Order.DoesNotExist:
                    order = None
                    return JsonResponse({'erorr': True,'mseeage' : '無此訂單'})
                return JsonResponse({'data':
                    {
                        'order' : order,
                        'trip_data' : trip_data,
                    }
                    , 'mseeage' : '取得成功'
                    })
            else :
                return JsonResponse({"error" : True, 'message' : '錯誤',})

        if request.method == 'GET':
            if user_name:
                try:
                    member = Member.objects.get(id = user_id)
                    # order = Order.objects.filter(user_id = member.id)
                    orders = member.order_set.all()
                    orders_list = []
                    for order in orders:
                        trip_data = Trip_data.objects.get(pk=order.trip_id.id)
                        trip_data = model_to_dict(trip_data)
                        data = {
                            'order' : model_to_dict(order),
                            'trip_data' : trip_data
                        }
                        orders_list.append(data)

                except Order.DoesNotExist:
                    return JsonResponse({"error" : True, 'message' : '無訂單',})
                return JsonResponse({'data': orders_list,'mseeage' : '登入中'})
            else :
                return JsonResponse({"error" : True, 'message' : '錯誤',})

        if request.method == 'POST':
            if user_name:
                data = request.body.decode('utf-8')
                data = json.loads(data)

                order_data = request.session.get('order')

                new_order = Order()
                new_order.user_id = Member.objects.get(user_email = user_email)
                new_order.trip_id = Trip_data.objects.get(pk=order_data['order_trip']['id'])
                new_order.trip_date = order_data["order_date"]
                new_order.trip_time = order_data["order_time"]
                new_order.trip_cost = order_data["order_price"]
                new_order.contact_name = data["order"]["contact"]["name"]
                new_order.contact_email = data["order"]["contact"]["email"]
                new_order.contact_phone = data["order"]["contact"]["phone"]
                new_order.payment = '未付款'
                new_order.prime =data["prime"]
                new_order.save()

                tappaypay_prime = paybyprime(data)
                if tappaypay_prime["status"] == 0:
                    new_order.payment="已付款"
                    new_order.save()

                    print('訂單成立')
                    return JsonResponse ({
                        "ok" : True,
                        "message" : "資料送出成功",
                        "data":
                            {
                                "number": new_order.id,
                                "payment":
                                {
                                    "status": 0,
                                    "message": "已付款"
                                }
                            }
                        })
                return JsonResponse ({"ok" : True, "message" : "資料送出成功"})


def thanks(request,num):
    return render(request, 'thankyou.html')

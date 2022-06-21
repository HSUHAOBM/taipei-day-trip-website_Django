from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from member.models import Member
from django.http import HttpResponseBadRequest, JsonResponse
from trip_data.models import Trip_data

import json

# Create your views here.

def main(request):
    return render(request, 'booking.html')

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
                print('........')

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


            # try:
            #     member = Member.objects.get(user_email = email)
            # except Member.DoesNotExist:
            #     member = None
            # if (member) :
            #     return JsonResponse({'error' : True, 'message' : '已註冊'})
            # else:
            #     if not user_name.strip() or not email.strip() or not password.strip():
            #         return JsonResponse ({"error": True, "message": "檢查輸入是否為空白!"})
            #     elif (len(user_name) > 20 or len(email) < 6 or len(password) > 12 ):
            #         return JsonResponse ({"error": True, "message": "輸入字元數不符合規定"})
            #     else:
            #         # hash
            #         password = password + keyword
            #         password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            #         new_member = Member()
            #         new_member.user_name = user_name
            #         new_member.user_email = email
            #         new_member.user_password = password
            #         new_member.save()
            #         request.session["user_name"] = user_name
            #         request.session["user_email"] = email

                    # return JsonResponse ({"ok": True, "message": "註冊成功"})

        if request.method == 'PATCH':
            data = request.body.decode('utf-8')
            data = json.loads(data)
            email = data['email']
            password = data['password']
            try:
                password = password + keyword
                password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                member = Member.objects.get(user_email = email, user_password = password)
                request.session["user_name"] = member.user_name
                request.session["user_email"] = member.user_email
                return JsonResponse ({"ok": True, "message": "登入成功"})

            except Member.DoesNotExist:
                return JsonResponse ({"error": True, "message": "信箱或密碼錯誤"})

        if request.method == 'DELETE':
            print(user_name,user_email)
            request.session.clear()
            return JsonResponse ({"ok": True, "message": "登出成功"})


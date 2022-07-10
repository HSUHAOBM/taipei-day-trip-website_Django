import json
import re
import os
import django
from django.core.wsgi import get_wsgi_application

import sys

def main():

    with open("data/taipei-attractions.json", "r", encoding="utf-8") as json_data:
        data = json.load(json_data)

    def getimg(a):  # 圖片篩選
        reg = "http.*?\.jpg"
        imgre = re.compile(reg)
        imglist_jgp = imgre.findall(a)
        #     print("imglist_jpg:",imglist_jgp)
        reg2 = "http.*?\.png"
        imgre2 = re.compile(reg2)
        imglist_png = imgre2.findall(a)
        #     print("imglist2_png:",imglist_png)
        return imglist_jgp + imglist_png

    print('資料數：',len(data["result"]["results"]))

    for i in range(len(data["result"]["results"])):
        models.Trip_data.objects.create(
            stitle = data["result"]["results"][i]["stitle"],
            category = data["result"]["results"][i]["CAT2"],
            description = data["result"]["results"][i]["xbody"],
            address = "".join(data["result"]["results"][i]["address"].split(" ")[0::2]),
            transport = data["result"]["results"][i]["info"],
            mrt = data["result"]["results"][i]["MRT"],
            latitude = data["result"]["results"][i]["latitude"],
            longitude = data["result"]["results"][i]["longitude"],
            images = ",".join(
                getimg(
                    ",http://".join(
                        data["result"]["results"][i]["file"].lower().split("http://")
                    )
                )
            ),
        )
    print('done')

if __name__ == "__main__":

    parent_dir = os.path.abspath(os.path.dirname(os.getcwd()))
    # print(parent_dir) #上層路徑

    sys.path.append(parent_dir)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taipei_trip.settings")
    application = get_wsgi_application()

    django.setup()
    from trip_data import models

    main()

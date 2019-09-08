#!/usr/bin/python
import requests
import base64
import json
import time

start = time.time()

# Sample image file is available at http://plates.openalpr.com/ea7the.jpg
indexfile = open('indexfile.txt', 'r')
index_number = indexfile.read()
index_number = int(index_number)
indexfile.close()
IMAGE_PATH = 'img.jpg'
Secret_keys_list = ['sk_0a6e5da191c8101e6df0d446','sk_f6e7a8f3e14efa99a5a484a8','sk_cb782bf31e4790a44fd7cda5','sk_d6d8b5d7be4e199555196f65']
SECRET_KEY = Secret_keys_list[index_number] 
with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())




try:
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=in&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    r = r.json()
    plate = r["results"][0]["plate"]
    print(plate)
    myfile = open("license plate.txt", 'w')
    myfile.write(plate)
    myfile.close()
    print(plate)
    if r["credits_monthly_used"] == r["credits_monthly_total"]:
        indexfile = open('indexfile.txt', 'w')
        if index_number == len(Secret_keys_list)-1 :
            indexfile.write(str(0))
        else:
            indexfile.write(index_number+1)
        indexfile.close()
    print(time.time()-start)

except:
    myfile = open('license plate.txt', 'w')
    myfile.write("Error")
    myfile.close()
    print(time.time()-start)


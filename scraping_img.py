# -*- encoding: utf-8 -*-

import json
from datetime import datetime

##############################################
## getImageUrls
## max_imagesの数だけ、search_qで見つけたURLを取得してreturnする
## 返り値：
## image_results["画像のサムネイルURL"]["画像のフルURL"]
##############################################
def getImageUrls(search_q="スーツ", max_images=50):
    # Azure のAPIを登録。
    from azure.cognitiveservices.search.imagesearch import ImageSearchAPI
    from msrest.authentication import CognitiveServicesCredentials
    # 環境設定
    apikey_file = "apikey.txt"
    with open(apikey_file) as f:
        key = f.readlines()
    subscription_key = key[0].strip()

    # 検索クエリ
    search_term = search_q
    # パラメータ
    img_count = 35
    #API Client
    client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))

    #max_imagesの数だけ画像を取得。
    for i in range(0,max_images // img_count):
        tmp_results = client.images.search(
            query=search_term,
            count=img_count,
            offset=(i*img_count))

    for tmp_img in tmp_results.Value:
        image_results.append = [
            tmp_img.thumbnail_url,
            tmp_img.content_url]


    return image_results

#時間データのdump化
def date_encoder(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()

##############################################
## main
##############################################
image_results = getImageUrls("スーツ")
json_results = open('result.json', 'w')
json.dump(image_results, json_results, indent=2, default=date_encoder)
if image_results.value:
    first_image_result = image_results.value[0]
    print("Total number of images returned: {}".format(len(image_results.value)))
    print("First image thumbnail url: {}".format(
        first_image_result.thumbnail_url))
    print("First image content url: {}".format(first_image_result.content_url))
    #print("total_Hits: {}".format(image_results.totalEstimatedMatches))
else:
    print("No image results returned!")

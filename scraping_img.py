# -*- encoding: utf-8 -*-

import numpy as np
import re
import requests
import http.client


def checkFileType(filename):
    '''
    渡されたファイルの末尾が画像以外のものは排除
    お蔵入り?
    '''
    regex = re.compile(r'((\.jpg)|(\.png)|(\.gif)|(\.bmp))$')
    match = regex.search(filename)
    if match is None:
        return False
    else:
        return True


def writeResults(results, file="imgs/default_results.txt"):
    '''
    リストで渡された結果を特定のファイルに書き込む
    '''
    with open(file, mode='w') as f:
        f.write("\n".join(results))


def getImageUrls(search_q="スーツ", max_images=30):
    '''
    max_imagesの数だけ、search_qで見つけたURLを取得してreturnする
    返り値：
    image_results["画像のサムネイルURL"]["画像のフルURL"]
    np.arrayで帰ってくる。
    '''
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
    img_count = 10
    # API Client
    client = ImageSearchAPI(CognitiveServicesCredentials(subscription_key))

    # max_imagesの数だけ画像を取得。
    # img_countごとに取得するが、端数は切り捨て。
    for i in range(0, max_images // img_count):
        tmp_results = client.images.search(
            query=search_term,
            count=img_count,
            offset=(i*img_count))

    # return用のオブジェクトを作成
    image_results = [["thumnail_url", "content_url"]]
    for tmp_img in tmp_results.value:
        image_results.append([
            tmp_img.thumbnail_url,
            tmp_img.content_url])

    # listをnp.arrayに変換してreturn
    return np.array(image_results)


def dlImages(img_list, save_path):
    '''画像をダウンロードする関数

    img_list=画像URLが格納されたlist
    save_path=画像を保存するパス
    ついでに同じディレクトリに_imgs_url.logを生成する。
    '''
    for img_url in len(img_list):
        response = requests(img_url, allow_redirect=True, timeout=10)
        if response.status_code != 200:
            error = Exception("responsed HTTP STATUS:" + response.status_code)
            raise error
        else:
            pass
        pass
    pass


if __name__ == '__main__:'
'''
    使えそうなクエリ候補
    写真：
    +filterui:photo-photo
    縦長：
    +filterui:aspect-tall
    スーツ+男性+filterui:photo-photo
    '''

image_results = getImageUrls("スーツ")
#writeResults(image_results[:, 0], "imgs/results_thumbnails.txt")
writeResults(image_results[:, 1], "imgs/results_contents.txt")

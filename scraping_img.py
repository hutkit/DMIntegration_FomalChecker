# -*- encoding: utf-8 -*-

import numpy as np
import requests
import os
import urllib
# import http.client


def writeResults(results, file="imgs/default_results.txt"):
    '''
    リストで渡された結果を特定のファイルに書き込む
    '''
    with open(file, mode='w') as f:
        f.write("\n".join(results))


def getImageUrls(search_q="スーツ", get_once_images=10, max_images=30):
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
    img_count = get_once_images
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
    image_results = []
    file_num = 0
    for tmp_img in tmp_results.value:
        image_results.append([
            str(file_num).zfill(5),
            tmp_img.thumbnail_url,
            tmp_img.content_url])
        file_num += 1

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


def download_image(url, timeout=10):
    response = requests.get(url, allow_redirects=True, timeout=timeout)
    if response.status_code != 200:
        error = Exception("HTTP status: " + response.status_code)
        raise error

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        error = Exception("Content-Type: " + content_type)
        raise error

    return response.content


def save_image(filename, image):
    with open(filename, "wb") as fout:
        fout.write(image)


def get_imgs_from_urlfile(urlfile, save_dir):
    with open(urlfile) as fobj:
        name_num = 0
        for f in fobj:
            url_parsed = urllib.parse.urlparse(f.rstrip("\n"))
            img_url = urllib.parse.urlunparse(url_parsed)
            ret_content = download_image(img_url)
            # ディレクトリ名 + 00000からの通し番号 + 拡張子.xxx
            name_str = save_dir + \
                str(name_num).zfill(5) + os.path.splitext(img_url)[-1]
            save_image(name_str, ret_content)
            name_num += 1


def run_scraping(dir, search_q):
    image_results = getImageUrls(search_q, 10, 30)
    writeResults(image_results[:, 0], dir + "results_numAndurl.txt")
    writeResults(image_results[:, 2], dir + "results_contents.txt")
    get_imgs_from_urlfile(dir + "results_contents.txt", dir)
    pass


if __name__ == '__main__':
    '''
    使えそうなクエリ候補
    写真：
    +filterui:photo-photo
    縦長：
    +filterui:aspect-tall
    スーツ+男性+filterui:photo-photo
    '''
    run_scraping("imgs/men_suit/", "男性+スーツ")

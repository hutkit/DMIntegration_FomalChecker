# -*- encoding: utf-8 -*-

'''
最低限データを保存する。
'''
import requests


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
            img_url = f.rstrip("\n")
            ret_content = download_image(img_url)
            # ディレクトリ名 + 00000からの通し番号 + 拡張子.xxx
            name_str = save_dir + str(name_num).zfill(5) + img_url[-4:]
            save_image(name_str, ret_content)
            ++name_num


##############################################################################
# main function
##############################################################################
if __name__ == '__main__':
    get_imgs_from_urlfile("testfiles.txt", "")
    pass

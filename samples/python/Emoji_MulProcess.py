import os
from time import time

import requests
from bs4 import BeautifulSoup
import multiprocessing

path = r'../../sourceimages' "\\"

def download_biaoqingbaos(url):

    response = requests.get(url)
    # lxml HTML解析器
    soup = BeautifulSoup(response.content, 'lxml')
    img_list = soup.find_all('img', class_='ui image lazy')

    for img in img_list:
        image = img.get('data-original')
        title = img.get('title')
        print('下载图片： ', title)

        try:
            # 分离文件名和扩展名，返回元组，取后缀名； wb表示以二进制写方式打开文件
            with open(path + title + os.path.splitext(image)[-1], 'wb') as f:
                img = requests.get(image).content
                f.write(img)
        except OSError:
            print('length  failed')
            break


if __name__ == '__main__':

    start = time()

    # 构建所有的链接
    _url = 'https://fabiaoqing.com/biaoqing/lists/page/{page}.html'
    urls = [_url.format(page=page) for page in range(1, 200+1)]

    if not os.path.exists(path):
        os.makedirs(path)

    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    # 将第二个参数的需要迭代的列表元素一个个地传入第一个参数的函数中
    pool.map(download_biaoqingbaos, urls)

    pool.close()

    pool.join()

    print('下载完毕耗时：  ', time()-start)
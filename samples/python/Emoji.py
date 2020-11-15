import os
from time import time

import requests
from bs4 import BeautifulSoup
from queue import Queue
from threading import Thread


class DownloadBiaoqingbao(Thread):

    def __init__(self, queue, path):
        Thread.__init__(self)
        self.queue = queue
        self.path = path
        if not os.path.exists(path):
            os.makedirs(path)

    def run(self):
        while True:
            url = self.queue.get()
            try:
                # print(url)
                download_biaoqingbaos(url, self.path)
            finally:
                self.queue.task_done()


def download_biaoqingbaos(url, path):

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

    queue = Queue()
    path = r'E:\workspace\python\tran\emoji' "\\"

    # 创建线程
    for x in range(10):
        worker = DownloadBiaoqingbao(queue, path)
        # 主线程运行结束时不对子线程进行检查而直接退出，同时该子线程随主线程一起结束，不论是否运行完成
        worker.daemon = True
        worker.start()

    # 加入队列
    for url in urls:
        queue.put(url)

    # 阻塞调用线程，直到队列中所有任务被处理掉，即每个任务调用task_done()方法结束自己任务
    queue.join()

    print('下载完毕耗时：  ', time()-start)
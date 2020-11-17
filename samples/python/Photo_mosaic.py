"""
* Emoji_MulProcess.py
* this class is for generating mosaic picture
* created by SA20225338 罗昊
* copyright USTC
* 15.11.2020
"""

# OpenCV库，用于解决计算机视觉问题的py库
import cv2
# python自带的操作文件的相关模块
import glob
# 命令行解析模块，可以直接中命令行中就可以向程序中传入参数并让程序运行
import argparse
# 用于机器学习中完成基础数值计算
import numpy as np
# 用于显示进度条
from tqdm import tqdm
# 用于解决排列组合问题，product用于求多个可迭代对象的笛卡尔积，跟嵌套的for循环等价
from itertools import product


"""
功能：命令行参数解析
@:return 命令行参数
"""
def parseArgs():
    # 创建ArgumentParser()对象
    parser = argparse.ArgumentParser('拼马赛克图片')
    # 调用add_argument()方法添加参数
    parser.add_argument('--targetpath', type=str, default='../../examples/input.jpg', help='目标图像路径')
    parser.add_argument('--outputpath', type=str, default='../../examples/output.jpg', help='输出图像路径')
    parser.add_argument('--sourcepath', type=str, default='../../sourceimages', help='用于拼接目标图像的所有源图像文件夹路径')
    parser.add_argument('--blocksize', type=int, default=15, help='马赛克块大小')
    # 解析参数
    args = parser.parse_args()
    return args


"""
功能：读取所有源图片并计算对应的颜色平均值
@:param sourcepath 源路径
@:param blocksize 块大小
@:return1 修改大小后的图片列表
@:return2 图片列表对应的颜色均值列表
"""
def readSourceImages(sourcepath, blocksize):
    print('Start to read source images')

    # 存储重置大小后的图片
    sourceimages = []
    # 记录每个图片的颜色均值
    avgcolors = []

    # 遍历指定文件夹中的jpg图片，并显示进度条
    for path in tqdm(glob.glob("{}/*.jpg".format(sourcepath))):

        # bug：使用cv2.imread读取含有中文路径的图片时，返回None
        # image = cv2.imread(path, cv2.IMREAD_COLOR)

        # 解决办法：先用np.fromfile()读取为np.uint8格式，再使用cv2.imdecode()解码。
        ffile = np.fromfile(path, dtype=np.uint8)

        if ffile.any():
            image = cv2.imdecode(ffile, -1)

        # shape[0]表示图片高度像素，[1]表示宽度像素，[2]为3时表示彩色图片
        if not ffile.any() or image is None or image.shape[-1] != 3:
            continue

        # 重置图片大小为blocksize*blocksize
        image = cv2.resize(image, (blocksize, blocksize))

        # 矩阵列求和(axis=0时),然后计算调整后的图片的颜色均值
        avgcolor = np.sum(np.sum(image, axis=0), axis=0) / (blocksize * blocksize)

        sourceimages.append(image)
        avgcolors.append(avgcolor)

    print('Finish reading source images')

    # np.array()用于将python数组转化为np数组，因为py数组的元素本质上是对象，对于数值运算比较浪费内存和cpu
    return sourceimages, np.array(avgcolors)


"""
功能：主函数
@:param args 命令行参数
"""
def main(args):

    # 读取图片文件，返回np.array类型
    targetimage = cv2.imread(args.targetpath)
    # 返回一个给定形状和类型的用0填充的数组
    outputimage = np.zeros(targetimage.shape, np.uint8)
    # 读源库中所有的表情包图片
    sourceimages, avgcolors = readSourceImages(args.sourcepath, args.blocksize)

    print('Start to make photomosaic')

    # 显示进度条，从左到右，从上到下遍历图片，每次截取马赛克块大小。shape[1]是宽度，shape[0]是高度
    for i, j in tqdm(product(range(int(targetimage.shape[1]/args.blocksize)), range(int(targetimage.shape[0]/args.blocksize)))):

        # 将图片分成一小块
        block = targetimage[j*args.blocksize: (j+1)*args.blocksize, i*args.blocksize: (i+1)*args.blocksize, :]

        # 求target图片每一小块的颜色均值
        avgcolor = np.sum(np.sum(block, axis=0), axis=0) / (args.blocksize * args.blocksize)

        # 求矩阵多个行向量的范数
        distances = np.linalg.norm(avgcolor - avgcolors, axis=1)

        # 该distances的list展平对应的水平方向最小值的下标
        idx = np.argmin(distances)

        # 设置输出图片对应块的马赛克图片为该最接近源图片颜色均值的图片
        outputimage[j*args.blocksize: (j+1)*args.blocksize, i*args.blocksize: (i+1)*args.blocksize, :] = sourceimages[idx]

    # 指定图片存储路径和文件名
    cv2.imwrite(args.outputpath, outputimage)

    # 在窗口中显示图像
    cv2.imshow('result', outputimage)
    # 等待用户按下按键，不加的话上面显示图像后一闪就消失了
    cv2.waitKey(0)
    # 销毁创建的所有窗口
    cv2.destroyAllWindows()

    print('Finish making photomosaic, result saved in %s' % args.outputpath)
 

'''run'''
if __name__ == '__main__':
    main(parseArgs())
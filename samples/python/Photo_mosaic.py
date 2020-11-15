import cv2
import glob
import argparse
import numpy as np
from tqdm import tqdm
from itertools import product


'''命令行参数解析'''
def parseArgs():
    parser = argparse.ArgumentParser('拼马赛克图片')
    parser.add_argument('--targetpath', type=str, default='../../examples/input.jpg', help='目标图像路径')
    parser.add_argument('--outputpath', type=str, default='../../examples/output.jpg', help='输出图像路径')
    parser.add_argument('--sourcepath', type=str, default='../../sourceimages', help='用于拼接目标图像的所有源图像文件夹路径')
    parser.add_argument('--blocksize', type=int, default=15, help='马赛克块大小')
    args = parser.parse_args()
    return args


'''读取所有源图片并计算对应的颜色平均值'''
def readSourceImages(sourcepath, blocksize):
    print('Start to read source images')
    sourceimages = []
    avgcolors = []
    for path in tqdm(glob.glob("{}/*.jpg".format(sourcepath))):
        # image = cv2.imread(path, cv2.IMREAD_COLOR)
        image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
        if image is None or image.shape[-1] != 3:
            continue
        image = cv2.resize(image, (blocksize, blocksize))
        avgcolor = np.sum(np.sum(image, axis=0), axis=0) / (blocksize * blocksize)
        sourceimages.append(image)
        avgcolors.append(avgcolor)
    print('Finish reading source images')
    return sourceimages, np.array(avgcolors)


'''主函数'''
def main(args):
    targetimage = cv2.imread(args.targetpath)
    outputimage = np.zeros(targetimage.shape, np.uint8)
    sourceimages, avgcolors = readSourceImages(args.sourcepath, args.blocksize)
    print('Start to make photomosaic')
    for i, j in tqdm(product(range(int(targetimage.shape[1]/args.blocksize)), range(int(targetimage.shape[0]/args.blocksize)))):
        block = targetimage[j*args.blocksize: (j+1)*args.blocksize, i*args.blocksize: (i+1)*args.blocksize, :]
        avgcolor = np.sum(np.sum(block, axis=0), axis=0) / (args.blocksize * args.blocksize)
        distances = np.linalg.norm(avgcolor - avgcolors, axis=1)
        idx = np.argmin(distances)
        outputimage[j*args.blocksize: (j+1)*args.blocksize, i*args.blocksize: (i+1)*args.blocksize, :] = sourceimages[idx]
    cv2.imwrite(args.outputpath, outputimage)
    cv2.imshow('result', outputimage)
    print('Finish making photomosaic, result saved in %s' % args.outputpath)


'''run'''
if __name__ == '__main__':
    main(parseArgs())
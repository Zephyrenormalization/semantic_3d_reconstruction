# extract frames from video and save them as images
import os
import cv2
import argparse

def padding_str_0(str,length):
    return '0'*(length-len(str))+str

def video2pic(video_path, output_dir,pic_num):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cap = cv2.VideoCapture(video_path)
    count = 0
    frame_num = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # 均匀采样
    step = frame_num // pic_num
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if count % step == 0:
            pic_name = padding_str_0(str(count),3)
            cv2.imwrite(os.path.join(output_dir, pic_name + '.png'), frame)
        count += 1
        if count >= pic_num:
            break
    cap.release()

def main():
    args = argparse.ArgumentParser()
    args.add_argument('--video_path', type=str, default='data/video/1.mp4')
    args.add_argument('--output_dir', type=str, default='data/pic')
    args.add_argument('--pic_num', type=int, default=150)
    opt = args.parse_args()
    video2pic(opt.video_path, opt.output_dir, opt.pic_num)

if __name__ == '__main__':
    main()
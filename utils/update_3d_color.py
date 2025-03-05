import argparse
import os
import cv2
from collections import Counter

def get_name2image(segmantic_fig_path):
    name2image = {}
    for file in os.listdir(segmantic_fig_path):
        if file.endswith(('.png', '.jpg', '.jpeg', '.bmp', 'JPG')):
            name = file
            image = cv2.imread(os.path.join(segmantic_fig_path, file))
            # image= cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            if image is None:
                raise ValueError(f'Cannot read image {file}')
            name2image[name] = image
    # print(name2image.keys())
    return name2image


def update_color(camera_txt_path ,imgage_txt_path, points_txt_path, segmantic_fig_path, output_dir):
    # 仅考虑citiscapes数据集，因为voc数据集类别中没有建筑
    rgb2cls = {
    'citiscapes': {
        (0, 0, 0): 'unlabeled',
        (111, 74, 0): 'dynamic',
        (81, 0, 81): 'ground',
        (128, 64, 128): 'road',
        (244, 35, 232): 'sidewalk',
        (250, 170, 160): 'parking',
        (230, 150, 140): 'rail track',
        (70, 70, 70): 'building',
        (102, 102, 156): 'wall',
        (190, 153, 153): 'fence',
        (180, 165, 180): 'guard rail',
        (150, 100, 100): 'bridge',
        (150, 120, 90): 'tunnel',
        (153, 153, 153): 'pole',
        (250, 170, 30): 'traffic light',
        (220, 220, 0): 'traffic sign',
        (107, 142, 35): 'vegetation',
        (152, 251, 152): 'terrain',
        (70, 130, 180): 'sky',
        (220, 20, 60): 'person',
        (255, 0, 0): 'rider',
        (0, 0, 142): 'car',
        (0, 0, 70): 'truck',
        (0, 60, 100): 'bus',
        (0, 0, 90): 'caravan',
        (0, 0, 110): 'trailer',
        (0, 80, 100): 'train',
        (0, 0, 230): 'motorcycle',
        (119, 11, 32): 'bicycle',
        (0, 0, 142): 'license plate',  # 注意：license plate 的颜色与 car 相同
    }
    }
    cls2rgb = {}
    cls2rgb['citiscapes'] = {v: k for k, v in rgb2cls['citiscapes'].items()}

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    name2image = get_name2image(segmantic_fig_path)
    with open(imgage_txt_path, 'r') as f:
        # Image list with two lines of data per image:
        # IMAGE_ID,QW,QX,QY,QZ,TX,TY,TZ,CAMERA ID,NAME
        # POINTS2D[]as(X，Y,POINT3D_ID)
        # 不读#开头的注释行

        image_lines = [line for line in f if not line.startswith('#')]
    with open(points_txt_path, 'r') as f:
        points_lines = [line for line in f if not line.startswith('#')]
    
    point3d_id2rgb = {}

    for (i, point_line) in zip(range(len(points_lines)), points_lines):
        # points3d_id, x, y, z, r, g, b, error, (image_id, points2d_id)
        point_line_list = point_line.strip().split()
        image_id2points2d_id = {point_line_list[i]: point_line_list[i + 1] for i in range(8, len(point_line_list), 2)}
        cls_list = []
        for image_id, points2d_id in image_id2points2d_id.items():
            image_id = int(image_id)
            image_line = [image_lines[2*image_id-2], image_lines[2*image_id-1]]
            image_line_list = [image_line[0].strip().split(), image_line[1].strip().split()]
            image_name = image_line_list[0][-1]
            image_name = image_name.split('.')[0] + '.png'
            image = name2image[image_name]
            points_2d_coordinate = (round(float(image_line_list[1][int(points2d_id)*3])), round(float(image_line_list[1][int(points2d_id)*3+1])))
            bgr = image[points_2d_coordinate[1], points_2d_coordinate[0]]
            rgb = tuple(reversed(bgr))
            cls_list.append(rgb2cls['citiscapes'][rgb])
        cls_counter = Counter(cls_list)
        # choose the most common class as the final class
        cls = cls_counter.most_common(1)[0][0]
        rgb = cls2rgb['citiscapes'][cls]
        point3d_id2rgb[point_line_list[0]] = rgb
    
    # write the result to output file
    # 先将原始文件写入
    with open(camera_txt_path, 'r') as f:
        camera_lines = f.readlines()
    with open(os.path.join(output_dir, 'cameras.txt'), 'w') as f:
        f.writelines(camera_lines)
    with open(os.path.join(output_dir, 'images.txt'), 'w') as f:
        f.writelines(image_lines)
    with open(os.path.join(output_dir, 'points3D.txt'), 'w') as f:
        f.writelines(points_lines)
    # 再将rgb写入
    with open(os.path.join(output_dir, 'points3D.txt'), 'w') as f:
        for (i, point_line) in zip(range(len(points_lines)), points_lines):
            point_line_list = point_line.strip().split()
            rgb_values = point3d_id2rgb[point_line_list[0]]
            point_line_list[4] = str(rgb_values[0])
            point_line_list[5] = str(rgb_values[1])
            point_line_list[6] = str(rgb_values[2])
            f.write(' '.join(point_line_list) + '\n')

            

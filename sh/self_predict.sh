#!/bin/bash

# 定义变量
INPUT_FOLDER="./data/self_collected"
DATASET="cityscapes"
MODEL="deeplabv3plus_mobilenet"
CKPT="checkpoints/best_deeplabv3plus_mobilenet_cityscapes_os16.pth"
OUTPUT_DIR="./semantic_data/self_collected"

# 执行命令
python predict.py --input $INPUT_FOLDER \
                  --dataset $DATASET \
                  --model $MODEL \
                  --ckpt $CKPT \
                  --save_val_results_to $OUTPUT_DIR
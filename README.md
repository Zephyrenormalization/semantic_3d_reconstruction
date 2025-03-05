# 计算机视觉研讨课大作业：语义三维重建
## quick start
`linux`操作系统下，安装`conda`，创建新环境，然后
```shell
# 点击demo.ipynb全部运行即可
```
`windows`操作系统下，需要将sh命令替换为bat命令，或者将sh中的命令逐条复制到命令行中依demo.ipynb的指示执行。

## 项目结构
```
project_root/
├── data/
│   └── given/                  # 给定数据集图片
│   └── self_collected/         # 自采数据集图片
├── output/
│   └── colmap/                 # colmap输出文件夹
│       └── given/
│           ├── cameras.txt
│           ├── images.txt
│           └── points3D.txt
│       └── self_collected/
│           ...
├── semantic_data/              # 使用deeplabv3获得的语义信息
│   └── given/
│    ...
├── semantic_output/            # 将语义信息整理进colmap输出文件夹
│   └── given/
│    ...
├── utils/                      # 工具函数
│   └── update_3d_color.py      # 更新3d点云的颜色
│   └── video2pic.py            # 从视频中抽帧
├── sh/                         # 存放linux上运行的shell脚本
│    ...
├── pic/                        # 存放docs中用到的图片
│    ...
├── docs/                       # 存放文档
│    ...
├── README.md                   # 项目说明
├── requirements.txt            # 项目依赖
├── demo.ipynb                  # 演示代码和说明
```
## 数据集来源
- [Dataset](https://www.maths.lth.se/matematiklth/personal/calle/dataset/dataset.html)
## Citation
```
@inproceedings{schoenberger2016sfm,
    author={Sch\"{o}nberger, Johannes Lutz and Frahm, Jan-Michael},
    title={Structure-from-Motion Revisited},
    booktitle={Conference on Computer Vision and Pattern Recognition (CVPR)},
    year={2016},
}

@inproceedings{schoenberger2016mvs,
    author={Sch\"{o}nberger, Johannes Lutz and Zheng, Enliang and Pollefeys, Marc and Frahm, Jan-Michael},
    title={Pixelwise View Selection for Unstructured Multi-View Stereo},
    booktitle={European Conference on Computer Vision (ECCV)},
    year={2016},
}

@article{chen2018encoder,
  title={Encoder-Decoder with Atrous Separable Convolution for Semantic Image Segmentation},
  author={Chen, Liang-Chieh and Zhu, Yukun and Papandreou, George and Schroff, Florian and Adam, Hartwig},
  journal={arXiv preprint arXiv:1802.02611},
  year={2018}
}
```



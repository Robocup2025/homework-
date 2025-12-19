本仓库包含计算机视觉作业三的全部实现，核心代码集中在homework3.py中。编写过程中首先遇到图片读取问题，最初使用 OpenCV 的cv2.imread函数，但多次出现无法读取的情况，排查发现是环境依赖和文件路径适配问题，因此改用 Pillow 库的Image.open函数，通过find_and_load_image函数自动查找当前目录图片（优先test_image.jpg），并处理格式转换和路径适配，确保图片稳定加载。
在算法实现阶段，Canny 边缘检测的非极大值抑制步骤中，梯度方向的离散化处理容易出现边缘漏检，通过将角度划分为 4 个区间并精准判断邻域像素关系，解决了该问题；Harris 角点检测中响应函数 R 的阈值选择直接影响检测效果，通过归一化处理和动态调整阈值，平衡了角点的数量和准确性。
代码实现时先通过find_and_load_image函数自动查找并加载当前目录的图片（优先test_image.jpg）；接着sobel_filter实现 Sobel 梯度算子并通过visualize_sobel生成sobel_result.png；canny_edge_detection整合高斯滤波、梯度计算、非极大值抑制和双阈值连接流程，由visualize_canny输出canny_result.png；harris_corner_detection通过二阶矩矩阵和响应函数 R 检测角点，visualize_harris生成harris_result.png；histogram_equalization完成直方图均衡化，visualize_hist_equal输出hist_equal_result.png。所有算法均通过主函数按流程执行
# 计算机视觉作业三：基础算法实现

本仓库包含了梯度算子（Sobel）、Canny边缘检测、Harris角点检测和直方图均衡化四种经典计算机视觉算法的手动实现。

功能介绍

Sobel 梯度检测: 计算图像在水平和垂直方向的梯度，并用梯度幅值来突出图像边缘。
Canny 边缘检测: 一种多阶段的边缘检测算法，能有效抑制噪声并精确检测边缘。
Harris 角点检测: 通过分析图像局部区域的灰度变化来识别角点。
直方图均衡化: 通过调整图像的灰度值分布，增强图像的对比度。

环境依赖

Python 3.x
numpy
matplotlib
pillow (PIL)

安装依赖：

```bash
pip install numpy matplotlib pillow

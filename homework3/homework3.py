from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
def find_and_load_image():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')
    image_files = [
        f for f in os.listdir(current_dir)
        if f.lower().endswith(image_extensions)
    ]
    if not image_files:
        print("错误：当前目录未找到任何图片文件（支持格式：jpg、png、bmp等）")
        print("请将图片放在与脚本相同的文件夹中")
        return None
    target_file = "test_image.jpg"
    if target_file in image_files:
        image_path = os.path.join(current_dir, target_file)
    else:
        image_path = os.path.join(current_dir, image_files[0])
        print(f"ℹ️ 提示：未找到test_image.jpg，将使用 {image_files[0]}")
    try:
        with Image.open(image_path) as img_pil:
            img_gray = img_pil.convert('L')  
            img = np.array(img_gray)
        print(f"成功加载图片：{os.path.basename(image_path)}，尺寸：{img.shape[1]}x{img.shape[0]}")
        return img
    except Exception as e:
        print(f"图片读取失败：{str(e)}")
        return None
def sobel_filter(img):
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    padded = np.pad(img, (1, 1), mode='edge')
    grad_x = np.zeros_like(img, dtype=np.float32)
    grad_y = np.zeros_like(img, dtype=np.float32)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            grad_x[i, j] = np.sum(padded[i:i+3, j:j+3] * sobel_x)
            grad_y[i, j] = np.sum(padded[i:i+3, j:j+3] * sobel_y)
    magnitude = np.sqrt(grad_x**2 + grad_y**2)
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    return grad_x, grad_y, magnitude
def visualize_sobel(img, magnitude):
    plt.figure(figsize=(10, 4))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('原图'), plt.axis('off')
    plt.subplot(122), plt.imshow(magnitude, cmap='gray'), plt.title('Sobel梯度幅值'), plt.axis('off')
    plt.tight_layout(), plt.savefig('sobel_result.png', dpi=150), plt.show()
def gaussian_kernel(size=5, sigma=1):
    kernel = np.zeros((size, size))
    center = size // 2
    for i in range(size):
        for j in range(size):
            dist = (i - center)**2 + (j - center)** 2
            kernel[i, j] = np.exp(-dist / (2 * sigma**2))
    return kernel / np.sum(kernel)
def canny_edge_detection(img):
    gauss_kernel = gaussian_kernel(size=5, sigma=1)
    padded = np.pad(img, (2, 2), mode='edge')
    gauss_img = np.zeros_like(img, dtype=np.float32)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            gauss_img[i, j] = np.sum(padded[i:i+5, j:j+5] * gauss_kernel)
    gauss_img = gauss_img.astype(np.uint8)
    grad_x, grad_y, mag = sobel_filter(gauss_img)
    dir = np.arctan2(grad_y, grad_x) * 180 / np.pi % 180
    nms_img = np.zeros_like(mag)
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            angle = dir[i, j]
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                nms_img[i, j] = mag[i, j] if mag[i, j] >= mag[i, j-1] and mag[i, j] >= mag[i, j+1] else 0
            elif 22.5 <= angle < 67.5:
                nms_img[i, j] = mag[i, j] if mag[i, j] >= mag[i-1, j+1] and mag[i, j] >= mag[i+1, j-1] else 0
            elif 67.5 <= angle < 112.5:
                nms_img[i, j] = mag[i, j] if mag[i, j] >= mag[i-1, j] and mag[i, j] >= mag[i+1, j] else 0
            else:
                nms_img[i, j] = mag[i, j] if mag[i, j] >= mag[i-1, j-1] and mag[i, j] >= mag[i+1, j+1] else 0
    nms_img = nms_img.astype(np.uint8)
    high_thresh = 100
    low_thresh = 50
    strong = nms_img > high_thresh
    weak = (nms_img >= low_thresh) & (nms_img <= high_thresh)
    edge_img = np.zeros_like(nms_img)
    edge_img[strong] = 255
    for i in range(1, img.shape[0]-1):
        for j in range(1, img.shape[1]-1):
            if weak[i, j] and np.any(strong[i-1:i+2, j-1:j+2]):
                edge_img[i, j] = 255
    return gauss_img, mag, nms_img, edge_img
def visualize_canny(img, gauss, mag, nms, edge):
    plt.figure(figsize=(16, 4))
    plt.subplot(141), plt.imshow(gauss, cmap='gray'), plt.title('1. 高斯滤波'), plt.axis('off')
    plt.subplot(142), plt.imshow(mag, cmap='gray'), plt.title('2. 梯度幅值'), plt.axis('off')
    plt.subplot(143), plt.imshow(nms, cmap='gray'), plt.title('3. 非极大值抑制'), plt.axis('off')
    plt.subplot(144), plt.imshow(edge, cmap='gray'), plt.title('4. Canny边缘'), plt.axis('off')
    plt.tight_layout(), plt.savefig('canny_result.png', dpi=150), plt.show()
def harris_corner_detection(img):
    img_float = img.astype(np.float32)
    grad_x, grad_y, _ = sobel_filter(img_float)
    Ix2 = np.zeros_like(img_float)
    Iy2 = np.zeros_like(img_float)
    IxIy = np.zeros_like(img_float)
    gauss_kernel = gaussian_kernel(size=3, sigma=2)
    padded_Ix2 = np.pad(grad_x**2, (1, 1), mode='edge')
    padded_Iy2 = np.pad(grad_y**2, (1, 1), mode='edge')
    padded_IxIy = np.pad(grad_x * grad_y, (1, 1), mode='edge')
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            Ix2[i, j] = np.sum(padded_Ix2[i:i+3, j:j+3] * gauss_kernel)
            Iy2[i, j] = np.sum(padded_Iy2[i:i+3, j:j+3] * gauss_kernel)
            IxIy[i, j] = np.sum(padded_IxIy[i:i+3, j:j+3] * gauss_kernel)
    k = 0.04
    det_M = Ix2 * Iy2 - IxIy**2
    trace_M = Ix2 + Iy2
    R = det_M - k * (trace_M**2)
    R_norm = (R - R.min()) / (R.max() - R.min())
    threshold = 0.01
    strong = R_norm > threshold
    corner = np.zeros_like(img)
    padded_R = np.pad(R_norm, (1, 1), mode='constant')
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if strong[i, j]:
                neighborhood = padded_R[i:i+3, j:j+3]
                if R_norm[i, j] == np.max(neighborhood):
                    corner[i, j] = 255
    return corner.astype(np.uint8)
def visualize_harris(img, corners):
    plt.figure(figsize=(10, 4))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('原图'), plt.axis('off')
    plt.subplot(122), plt.imshow(img, cmap='gray'), plt.imshow(corners, cmap='jet', alpha=0.5)
    plt.title('Harris角点检测'), plt.axis('off')
    plt.tight_layout(), plt.savefig('harris_result.png', dpi=150), plt.show()
def histogram_equalization(img):
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf = cdf / cdf[-1] 
    eq_img = np.interp(img.flatten(), bins[:-1], cdf * 255).reshape(img.shape)
    return eq_img.astype(np.uint8)
def visualize_hist_equal(img, eq_img):
    plt.figure(figsize=(12, 6))
    plt.subplot(221), plt.imshow(img, cmap='gray'), plt.title('原图'), plt.axis('off')
    plt.subplot(223), plt.imshow(eq_img, cmap='gray'), plt.title('均衡化后图'), plt.axis('off')
    plt.subplot(222), plt.hist(img.flatten(), 256, [0, 256], color='gray'), plt.title('原直方图')
    plt.subplot(224), plt.hist(eq_img.flatten(), 256, [0, 256], color='gray'), plt.title('均衡化直方图')
    plt.tight_layout(), plt.savefig('hist_equal_result.png', dpi=150), plt.show()

if __name__ == "__main__":
    img = find_and_load_image()
    if img is None:
        sys.exit(1)  
    print("\n 正在执行Sobel梯度检测...")
    _, _, sobel_mag = sobel_filter(img)
    visualize_sobel(img, sobel_mag)
    print("\n 正在执行Canny边缘检测...")
    gauss, mag, nms, edge = canny_edge_detection(img)
    visualize_canny(img, gauss, mag, nms, edge)
    print("\n 正在执行Harris角点检测...")
    corners = harris_corner_detection(img)
    visualize_harris(img, corners)
    print("\n 正在执行直方图均衡化...")
    eq_img = histogram_equalization(img)
    visualize_hist_equal(img, eq_img)

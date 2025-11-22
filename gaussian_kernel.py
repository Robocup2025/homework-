import numpy as np
import matplotlib.pyplot as plt
import cv2
def gaussian_2d(ksize, sigma):
    """手动实现二维高斯核"""
    x, y = np.meshgrid(np.arange(-ksize//2, ksize//2+1),
                       np.arange(-ksize//2, ksize//2+1))
    g = np.exp(-(x**2 + y**2)/(2*sigma**2))
    g = g / g.sum()
    return g
params = [(3, 1), (5, 2), (7, 3)]
for ksize, sigma in params:
    manual_kernel = gaussian_2d(ksize, sigma)
    cv_kernel = cv2.getGaussianKernel(ksize, sigma)
    cv_kernel = cv_kernel @ cv_kernel.T
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(manual_kernel, cmap='jet')
    plt.title(f'Manual Kernel (ksize={ksize}, σ={sigma})')
    plt.colorbar()
    plt.subplot(1, 2, 2)
    plt.imshow(cv_kernel, cmap='jet')
    plt.title(f'OpenCV Kernel (ksize={ksize}, σ={sigma})')
    plt.colorbar()
    plt.tight_layout()
    plt.savefig(f'kernel_{ksize}_{sigma}.png')
    plt.show()

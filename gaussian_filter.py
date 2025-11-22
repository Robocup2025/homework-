import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def gaussian_2d(ksize, sigma):
    x, y = np.meshgrid(np.arange(-ksize//2, ksize//2+1),
                       np.arange(-ksize//2, ksize//2+1))
    g = np.exp(-(x**2 + y**2)/(2*sigma**2))
    return g / g.sum()
def conv2d(image, kernel):
    ksize = kernel.shape[0]
    pad = ksize // 2
    image_pad = np.pad(image, pad, mode='constant')
    result = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = (image_pad[i:i+ksize, j:j+ksize] * kernel).sum()
    return result
image = Image.open('kernel_3_1.png').convert('L')
image = np.array(image)
params = [(3, 1), (5, 2), (7, 3)]
for ksize, sigma in params:
    kernel = gaussian_2d(ksize, sigma)
    filtered_manual = conv2d(image, kernel)
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.subplot(1, 3, 2)
    plt.imshow(filtered_manual, cmap='gray')
    plt.title(f'Manual Filter (ksize={ksize}, σ={sigma})')
    plt.tight_layout()
    plt.savefig(f'filter_{ksize}_{sigma}.png')
    plt.show()

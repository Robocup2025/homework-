import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
def zero_padding(image, pad_size):
    return np.pad(image, pad_size, mode='constant', constant_values=0)
def replicate_padding(image, pad_size):
    return np.pad(image, pad_size, mode='edge')
image = Image.open('kernel_3_1.png').convert('L')
image = np.array(image)
pad_size = 20
zero_pad = zero_padding(image, pad_size)
replicate_pad = replicate_padding(image, pad_size)
plt.figure(figsize=(12, 5))
plt.subplot(1, 3, 1)
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.subplot(1, 3, 2)
plt.imshow(zero_pad, cmap='gray')
plt.title('Zero Padding')
plt.subplot(1, 3, 3)
plt.imshow(replicate_pad, cmap='gray')
plt.title('Replicate Padding')
plt.tight_layout()
plt.savefig('padding_results.png')
plt.show()

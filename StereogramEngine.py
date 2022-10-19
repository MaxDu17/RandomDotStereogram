import matplotlib.pyplot as plt
import numpy as np
import imageio
from skimage.transform import resize

NUMBER_POINTS = 5000
SIZE = 1
RESOLUTION = 512


im = imageio.imread("test.png")
im = resize(im, (512, 512))[:, :, :-1] #remove the alpha channel
im = np.mean(im, axis = 2)
mask = im < 0.5
mask = np.rot90(mask, k = 3)


x_list = np.random.random((NUMBER_POINTS)) * RESOLUTION
y_list = np.random.random((NUMBER_POINTS)) * RESOLUTION
shifted_x_list = x_list.copy()
shifted_x_list -= 0.01 * RESOLUTION

for i in range(len(x_list)):
    nearest_x = int(x_list[i])
    nearest_y = int(y_list[i])
    if mask[nearest_x, nearest_y]:
        shifted_x_list[i] -= 0.01 * RESOLUTION

    # if 0.25 < x_list[i] < 0.75 and 0.25 < y_list[i] < 0.75:
    #     shifted_x_list[i] -= 0.01

plt.scatter(x_list, y_list, s = SIZE, color = "#3AF2F8", alpha = 0.8)
plt.scatter(shifted_x_list - 0.01, y_list, s = SIZE, color = "#ff370f", alpha = 0.8)

plt.show()


# for i in range(NUMBER_POINTS):
#     points_list
#


import matplotlib.pyplot as plt
import numpy as np
import imageio
from skimage.transform import resize
import io
from scipy.ndimage.interpolation import rotate

NUMBER_POINTS = 5000
SIZE = 1
RESOLUTION = 512

def make_random_scatter(depth_map):
    # depth map should go from 0 to 1
    x_list = np.random.random((NUMBER_POINTS)) * RESOLUTION
    y_list = np.random.random((NUMBER_POINTS)) * RESOLUTION
    shifted_x_list = x_list.copy()
    shifted_x_list -= 0.005 * RESOLUTION

    for i in range(len(x_list)):
        nearest_x = int(x_list[i])
        nearest_y = int(y_list[i])
        shifted_x_list[i] -= 0.015 * depth_map[nearest_x, nearest_y] * RESOLUTION #radius_from_center

    return x_list, shifted_x_list, y_list

def rotate_image(filename, savename):
    im = imageio.imread(filename)
    im = resize(im, (RESOLUTION, RESOLUTION))[:, :, :-1]  # remove the alpha channel
    im = np.mean(im, axis=2)
    depth_map = 1 - im
    depth_map = np.rot90(depth_map, k=3).astype(np.float32)

    writer = imageio.get_writer(f"{savename}.gif", fps=20)
    for i in range(100):
        rotated_map = rotate(depth_map, angle=(i / 100) * 359)
        print(i)
        fig, ax = plt.subplots()
        x_list, shifted_x_list, y_list = make_random_scatter(rotated_map)
        ax.scatter(x_list, y_list, s=SIZE, color="#3AF2F8", alpha=0.8)
        ax.scatter(shifted_x_list, y_list, s=SIZE, color="#ff370f", alpha=0.8)
        with io.BytesIO() as buff:
            fig.savefig(buff, format='raw')
            buff.seek(0)
            w, h = fig.canvas.get_width_height()
            data = np.frombuffer(buff.getvalue(), dtype=np.uint8)
            im = data.reshape((int(h), int(w), -1))
            writer.append_data(im)  # grayscale rendering
        plt.close(fig)

    writer.close()

def simple_render(filename, savename):
    im = imageio.imread(filename)
    im = resize(im, (RESOLUTION, RESOLUTION))[:, :, :-1]  # remove the alpha channel
    im = np.mean(im, axis=2)
    depth_map = 1 - im
    depth_map = np.rot90(depth_map, k=3).astype(np.float32)
    x_list, shifted_x_list, y_list = make_random_scatter(depth_map)

    fig, ax = plt.subplots()
    ax.scatter(x_list, y_list, s=SIZE, color="#3AF2F8", alpha=0.8)
    ax.scatter(shifted_x_list, y_list, s=SIZE, color="#ff370f", alpha=0.8)
    fig.savefig(f"{savename}.png")
    plt.close()

def depth_demo(savename):
    frequency = 3
    input_map = 2 * 3.14 * frequency * np.arange(RESOLUTION) / RESOLUTION
    input_map = np.tile(np.expand_dims(input_map, axis = 0), (RESOLUTION, 1))
    cycles_in_anim = 10

    writer = imageio.get_writer(f"{savename}.gif", fps=20)
    for i in range(100):
        input_map += (2 * 3.14 * cycles_in_anim) * (1 / 100)
        depth_map = (np.sin(input_map) + 1) / 2
        print(i)
        fig, ax = plt.subplots()
        x_list, shifted_x_list, y_list = make_random_scatter(depth_map)
        ax.scatter(x_list, y_list, s=SIZE, color="#3AF2F8", alpha=0.8)
        ax.scatter(shifted_x_list, y_list, s=SIZE, color="#ff370f", alpha=0.8)
        with io.BytesIO() as buff:
            fig.savefig(buff, format='raw')
            buff.seek(0)
            w, h = fig.canvas.get_width_height()
            data = np.frombuffer(buff.getvalue(), dtype=np.uint8)
            im = data.reshape((int(h), int(w), -1))
            writer.append_data(im)  # grayscale rendering
        plt.close(fig)

    writer.close()


if __name__ == "__main__":
    simple_render("whale.png", "whale_dot")
    # depth_demo("sine")
    # rotate_image("whale.png", "bouncing_whale")

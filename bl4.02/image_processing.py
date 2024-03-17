# 本示例展示了使用 Python 在 Blender 的图像上进行图像处理的高效方式。

import bpy
import numpy as np

# 定义输入图像名称和输出图像名称
input_image_name = "Image"
output_image_name = "NewImage"

# 获取输入图像
input_image = bpy.data.images[input_image_name]
w, h = input_image.size

# 分配一个 numpy 数组来操作像素数据
pixel_data = np.zeros((w, h, 4), 'f')

# 从 bpy.data 快速复制像素数据到 numpy 数组
input_image.pixels.foreach_get(pixel_data.ravel())

# 在这里使用 numpy 进行任何你想要的图像处理：
# 示例 1: 反转红、绿和蓝通道。
pixel_data[:, :, :3] = 1.0 - pixel_data[:, :, :3]
# 示例 2: 改变红通道的 Gamma 值。
pixel_data[:, :, 0] = np.power(pixel_data[:, :, 0], 1.5)

# 创建输出图像
if output_image_name in bpy.data.images:
    output_image = bpy.data.images[output_image_name]
else:
    output_image = bpy.data.images.new(output_image_name, width=w, height=h)

# 将像素数据从 numpy 数组复制回输出图像
output_image.pixels.foreach_set(pixel_data.ravel())
output_image.update()

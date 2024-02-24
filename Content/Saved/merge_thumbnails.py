import os
import json
from PIL import Image, ImageOps

# 定义合并图像的函数
def merge_images(image_paths):
    # 获取图像数量
    num_images = len(image_paths)

    # 计算幂次
    n = 0
    while 2 ** n < num_images:
        n += 1

    # 计算宫格大小
    grid_size = 2 ** n

    # 创建新图像
    new_image = Image.new('RGB', (grid_size * 256, grid_size * 256), (0, 0, 0))

    # 循环遍历每个格子
    for i in range(grid_size):
        for j in range(grid_size):
            # 计算当前格子对应的图像路径
            image_index = i * grid_size + j
            if image_index < num_images:
                image_path = image_paths[image_index]
            else:
                image_path = None

            # 打开图像并复制到新图像中
            if image_path:
                image = Image.open(image_path)
                # 根据宫格大小缩放图像
                image = ImageOps.fit(image, (256 // grid_size, 256 // grid_size), Image.Resampling.LANCZOS)
                # image = ImageOps.fit(image, (256 // grid_size, 256 // grid_size), method=Image.ANTIALIAS)                                                                          ^^^^^^^^^^^^^^^
                # AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'
                new_image.paste(image, (j * 256 // grid_size, i * 256 // grid_size))

            # 记录格子对应的原图名称
            grid_name = f"{i},{j}"
            if image_path:
                grid_map[grid_name] = os.path.basename(image_path)
            else:
                grid_map[grid_name] = None

    # 返回新图像
    return new_image

# 获取输入的TGA文件路径
tga_dir = input("请输入TGA文件所在目录路径：")

# 获取TGA文件路径列表
tga_paths = [os.path.join(tga_dir, f) for f in os.listdir(tga_dir) if f.endswith('.TGA')]

# 创建格子对应原图名称的映射
grid_map = {}

# 每n张图合并为一张图
n = int(input("请输入每n张图合并为一张图："))
num_images = len(tga_paths)
num_groups = (num_images + n - 1) // n

print("获取当前组的图像路径列表")
print(range(num_groups))
for i in range(num_groups):
    # 获取当前组的图像路径列表
    start_index = i * n
    end_index = min(start_index + n, num_images)
    group_paths = tga_paths[start_index:end_index]

    # 合并图像
    print("合并图像")
    merged_image = merge_images(group_paths)

    # 保存合并后的图像
    print("保存合并后的图像")
    merged_image.save(f"merge_{i+1}.png")

    # 保存格子对应原图名称的映射为JSON文件
    with open(f"grid_map_{i+1}.json", 'w') as f:
        json.dump(grid_map, f)

    # 清空格子对应原图名称的映射
    grid_map = {}
from PIL import Image, ImageOps
import os

# 高斯卷积核
gaussian_kernel = [
    [1, 2, 1],
    [2, 4, 2],
    [1, 2, 1]
]

# 批量处理PNG图片
def batch_process_png(input_folder, output_folder):
    # 遍历输入文件夹中的所有PNG文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            print('正在处理文件：', filename)
            # 打开PNG文件
            image = Image.open(os.path.join(input_folder, filename))
            # 将背景色置为透明
            image = image.convert('RGBA')
            newData = []

            origin_height = image.height
            origin_width = image.width

            # Upsample Image
            upscale = 2
            image = ImageOps.fit(image, (origin_height * upscale, origin_height * upscale), Image.Resampling.LANCZOS)

            data = image.getdata()
            for y in range(image.height):
                for x in range(image.width):
                    # 获取当前像素及其周围相邻像素的颜色值
                    neighbors = []
                    for j in range(-1, 2):
                        for i in range(-1, 2):
                            if x+i < 0 or x+i >= image.width or y+j < 0 or y+j >= image.height:
                                continue
                            pixel = data[(y+j)*image.width + (x+i)]
                            neighbors.append(pixel)



                    # 判断是否将像素点设为透明
                    pixel = data[y*image.width + x]

                    compare_color = []
                    compare_color.append( 0 ) #R
                    compare_color.append( 1 ) #G
                    compare_color.append( 0 ) #B

                    
                    isAlpha = pixel[0] == compare_color[0] and pixel[1] == compare_color[1] and pixel[2] == compare_color[2]

                    # 计算周围像素点的透明度平均值
                    r_sum = 0
                    r_count = 0
                    g_sum = 0
                    g_count = 0
                    b_sum = 0
                    b_count = 0
                    for neighbor in neighbors:
                        r_sum += neighbor[0]
                        g_sum += neighbor[1]
                        b_sum += neighbor[2]
                        if neighbor[0] > 0:
                            r_count += 1
                        if neighbor[1] > 0:
                            g_count += 1
                        if neighbor[2] > 0:
                            b_count += 1
                    if r_count >0 :
                        r_avg = r_sum / r_count
                    else:
                        r_avg = 0
                    if g_count >0 :
                        g_avg = g_sum / g_count
                    else:
                        g_avg = 0
                    if b_count >0 :
                        b_avg = b_sum / b_count
                    else:
                        b_avg = 0

                    
                    isAlpha |= r_avg <= compare_color[0] + 0.5 and g_avg <= compare_color[0] + 0.5 and b_avg <= compare_color[0] + 0.5

                    if isAlpha:
                        newData.append((0, 0, 0, 0))
                    else:
                        newData.append(pixel)
            
            image.putdata(newData)
            image = ImageOps.fit(image, (origin_height, origin_width), Image.Resampling.LANCZOS)
            # 保存为RGBA的PNG文件
            new_filename = filename.replace('_RGBA', '')
            new_filename = filename.replace('.png', '_RGBA.png')
            image.save(os.path.join(output_folder, new_filename), "PNG")
            print('保存文件：', new_filename, '成功')

# 示例使用
input_folder = input("请输入输入文件夹路径：")
output_folder = input_folder
#input("请输入输出文件夹路径：")
batch_process_png(input_folder, output_folder)
from PIL import Image
# pip install Pillow
import os

# 批量处理PNG图片
def batch_process_png(input_folder, output_folder):
    # 遍历输入文件夹中的所有PNG文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.PNG') and 'RGB' in filename:
            # 打开PNG文件
            image = Image.open(os.path.join(input_folder, filename))
            # 将背景色置为透明
            image = image.convert('RGBA')
            data = image.getdata()
            newData = []
            for item in data:
                if item[0] == 0 and item[1] == 1 and item[2] == 0:
                    newData.append((0, 0, 0, 0))
                else:
                    newData.append(item)
            image.putdata(newData)
            # 保存为RGBA的PNG文件
            new_filename = filename.replace('RGB', 'RGBA')
            image.save(os.path.join(output_folder, new_filename), "PNG")

# 示例使用
input_folder = input("请输入输入文件夹路径：")
output_folder = input_folder + "\\RGBA"
#input("请输入输出文件夹路径：")
batch_process_png(input_folder, output_folder)
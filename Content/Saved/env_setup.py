import subprocess
import sys

# 获取输入的Python可执行文件路径和要安装的库名列表
python_exe = input("请输入Python可执行文件路径：")
library_names = input("请输入要安装的库名，多个库名以';'分隔：").split(';')

# 使用subprocess模块调用pip安装库
for library_name in library_names:
    try:
        subprocess.check_call([python_exe, '-m', 'pip', 'install', library_name])
        print(f"{library_name}库安装成功！")
    except subprocess.CalledProcessError:
        print(f"{library_name}库安装失败！")
        sys.exit(1)
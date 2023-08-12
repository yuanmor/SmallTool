import sys
import os
import threading
from collections import OrderedDict

def remove_duplicates(file_path):
    # 读取原始文件并去除行末尾的换行符
    with open(file_path, 'r',errors='ignore') as file:
        lines = [line.rstrip('\n') for line in file]

    # 去重并保持顺序
    unique_lines = list(OrderedDict.fromkeys(lines))

    # 获取去重文件的路径和名称
    directory = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    new_filename = os.path.splitext(filename)[0] + "_OK.txt"
    new_file_path = os.path.join(directory, new_filename)

    # 写入去重结果到新文件，添加换行符
    with open(new_file_path, 'w') as new_file:
        new_file.write('\n'.join(unique_lines) + '\n')

    print(f"去重完成，去重文件保存在: {new_file_path}")
    with open(new_filename,"r", errors='ignore') as f:
        n = len(f.readlines())
    with open(file_path,"r", errors='ignore') as f:
        yn = len(f.readlines())
    print("原文件{0}行，\n去重后{1}行,\n总消除行数：{2}行".format(yn,n,yn-n))


# 其他代码...





def process_file(file_path, num_threads):
    # 检查文件扩展名是否为txt
    if not file_path.lower().endswith(".txt"):
        print("仅支持txt格式的文件。")
        return

    # 检查文件是否存在
    if not os.path.isfile(file_path):
        print("文件不存在。")
        return

    # 去重并保存结果
    remove_duplicates(file_path)

def main():
    # 获取文件路径和线程数参数
    file_path = None
    num_threads = 100  # 默认线程数为100

    if "-f" in sys.argv:
        file_index = sys.argv.index("-f") + 1
        if file_index < len(sys.argv):
            file_path = sys.argv[file_index]

    if "-t" in sys.argv:
        thread_index = sys.argv.index("-t") + 1
        if thread_index < len(sys.argv):
            try:
                num_threads = int(sys.argv[thread_index])
            except ValueError:
                print("无效的线程数参数。")
                sys.exit(1)

    # 检查文件路径参数
    if file_path is None:
        print("请通过参数 -f 提供要去重的文件路径。")
        sys.exit(1)

    # 处理文件
    process_file(file_path, num_threads)

if __name__ == "__main__":
    main()

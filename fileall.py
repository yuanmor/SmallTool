import os
import shutil
import argparse

def fun1(src_path, dst_path, file_name):
    count = 1
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.lower() == file_name.lower():  # Compare case-insensitive
                src_file_path = os.path.join(root, file)
                dst_file_path = os.path.join(dst_path, file)
                while os.path.exists(dst_file_path):
                    count += 1
                    dst_file_path = os.path.join(dst_path, str(count) + '_' + file)
                shutil.move(src_file_path, dst_file_path)
    print("执行完毕")

def main():
    parser = argparse.ArgumentParser(description="Process file or URL")
    parser.add_argument("-f", "--move_file", help="需要集合的文件名")
    parser.add_argument("-src", "--src_path", help="指定文件夹(自动探索子文件夹)")
    parser.add_argument("-dst", "--dst_path", help="指定输出地址")
    args = parser.parse_args()

    fun1(args.src_path,args.dst_path,args.move_file)


if __name__ == "__main__":
    main()

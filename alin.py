import os
import argparse
from tkinter.ttk import Style

from colorama import Fore
import argparse
import requests
import json
import csv


def json_xls(file):
    file_path = os.path.abspath(file)
    file_dirpath = os.path.dirname(file_path)
    csv_file = file_dirpath + "//json_csv.csv"

    with open(file_path,'r') as f:
        lines=f.readlines()

    k = json.loads(lines[0])
    keys = k.keys()
    karr = []
    for key in keys:
        karr.append(key)
    for line in lines:
        line = json.loads(line)
        with open(csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=karr)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(line)
    print("结束")





def get_absolute_path(file_path):
    absolute_path = os.path.abspath(file_path)
    return absolute_path
current_file_dir = os.path.dirname(os.path.abspath(__file__))

error1 = "语法有误，请使用-h查看帮助信息"
# 自定义帮助信息格式
class CustomFormatter(argparse.HelpFormatter):
    os.system("cls")
    test1 = Fore.GREEN + " 使用方法1:txt去重:" + Fore.LIGHTRED_EX +"\n\t命令：alint -f txt文件 -quchong\n\n"
    test2 = Fore.GREEN + "使用方法2：指定文件夹内，同名文件集合到指定目录--详情看介绍2:" + Fore.LIGHTRED_EX +"\n\t命令：alint -f 文件名 -src 指定搜索目录 -dst 指定输出目录\n\n"
    test3 = Fore.GREEN + "使用方法3：目录/敏感文件字典合并再分类--详情看介绍3" + Fore.LIGHTRED_EX +"\n\t命令：alint -f 合并后的txt文件名 -txt_class\n\n"
    test4 = Fore.GREEN + "使用方法4：jsfinder的结果集做分类--详情看介绍4" + Fore.LIGHTRED_EX +"\n\t命令：alint -f jsfinder结果集文件名（需要是txt） --jsfinder_class\n\n"
    test5 = Fore.GREEN + "使用方法5：url的存活探测" + Fore.LIGHTRED_EX +"\n\t命令：alint -f url文件 --urlbatch -x 404,500\n\n"
    test6 = Fore.GREEN + "使用方法6：json转csv" + Fore.LIGHTRED_EX +"\n\t命令：alint -f json文件 --json_csv\n\n"
    print(
        "帮助信息如下：\n" +
        Fore.YELLOW +
        "-f                 传入文件\n" +
        "-src               指定文件夹(自动探索子文件夹\n" +
        "-dst               指定输出地址\n" +
        "-urlbatct          检测url存活\n" +
        "-quchong           txt去重\n" +
        "-t                 指定线程数，方法1，3，5能使用，其他俩忘了加了，后面试了试，也没啥必要好像，就算了，需要自己加\n" +
        "-jsfinder_class    对jsfidner的结果集做分类，看介绍4\n" +
        "-txt_class         看介绍3\n"       
        "-x                 排除状态码，可排除多个，用逗号分割，请看使用方法5\n\n\n" + test1,test2,test3,test4,test5,test6 + Fore.WHITE +
        "介绍2：通过-f传入一个文件名，在-src指定的目录中收集所有同名的文件保存到-dst指定的位置\n\n介绍3：主要是有些小字典太乱了，可以将所有字典合在一起，然后它会自动对后缀进行分类，并以后缀命名，如：jsp.txt。没有后缀的一律写入path.txt，当然，如果你有很稀有的后缀，请到text_class.py文件中添加一下\n\n介绍4：将jsfinder的结果输出到一个txt中，然后对这个文件做一个分类，放到一个xls中，试试就知道了\n\n"

    )








def main():
    parser = argparse.ArgumentParser(formatter_class=CustomFormatter)
    parser.add_argument('-f', '--file', help='传入文件')
    parser.add_argument('-src','--src_path')
    parser.add_argument('-dst','--dst_path')
    parser.add_argument('-urlbatch','--urlbatch', action='store_true')
    parser.add_argument('-quchong','--quchong', action='store_true')
    parser.add_argument('-t','--thread')
    parser.add_argument('-jsfinder_class','--jsfinder_class', action='store_true')
    parser.add_argument('-txt_class','--txt_class', action='store_true')
    parser.add_argument('-x','--exclude')
    parser.add_argument('-jc','--json_csv',action='store_true',help="json转csv")
    args = parser.parse_args()
    args.thread=20
    if args.file:
        file_path = get_absolute_path(args.file)
        if args.quchong and args.txt_class:
            print("--quchong和txt_clss这俩参数不能一起用，去-h看帮助信息")
            return
        elif args.quchong:#方法一
            os.system("python {2}\\quchong.py -f {0} -t {1}".format(file_path,args.thread,current_file_dir))
            return
        elif args.txt_class:#方法三
            if args.thread:
                os.system("python {2}\\text_class.py -f {0} -t {1}".format(file_path, args.thread, current_file_dir))
                return
            else:
                os.system("python {1}\\text_class.py -f {0}".format(file_path, current_file_dir))
                return
        elif args.jsfinder_class:#方法四
            print("如果有报错：Error: 'utf-8' codec can't decode byte 0xc9 in position 50: invalid continuation byte，请修改jsfinder结果集的文件编码格式为utf-8")
            os.system("python {1}\\jsfinder_class.py -f {0}".format(file_path,current_file_dir))
            return
        elif args.src_path and args.dst_path:#方法2
            os.system("python {1}\\fileall.py -f {0} -src {2} -dst {3}".format(args.file,current_file_dir,args.src_path,args.dst_path))
            return
        elif args.urlbatch:#方法5
            if args.thread:
                if args.exclude:
                    os.system("python {0}\\urlbatch.py -f {1} -x {3} -t {2}".format(current_file_dir, file_path, args.thread,args.exclude))
                    return
                os.system("python {0}\\urlbatch.py -f {1} -x {3} -t {2}".format(current_file_dir, file_path, args.thread,1000))
                return
            else:
                if args.exclude:
                    os.system("python {0}\\urlbatch.py -f {1} -x {2}".format(current_file_dir, file_path,args.exclude))
                    return
                os.system("python {0}\\urlbatch.py -f {1} -x {2}".format(current_file_dir, file_path,1000))
                return
        elif(args.json_csv):
            json_xls(args.file)
            return
        else:
            print("参数有误，执行-h 查看帮助信息吧")
            return

if __name__ == "__main__":
    main()

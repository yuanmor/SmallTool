import argparse
import csv
import os
import shutil
import sys
import time

import chardet
import requests
from colorama import init, Fore
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

init(autoreset=True)

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    # 添加更多的User-Agent头
]

lock = threading.Lock()
exception_counter = 0


def check_url(url, exclude_codes, n, urls_len):
    global user_agents, exception_counter

    try:
        user_agent = user_agents.pop(0)
        user_agents.append(user_agent)

        headers = {
            "User-Agent": user_agent
        }

        response = requests.get(url, headers=headers, timeout=5)
        encoding = chardet.detect(response.content)['encoding']
        if response.status_code not in exclude_codes:
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding='utf-8')

            title = soup.title.string.strip() if soup.title else "该网站无标题"
            status_code = response.status_code

            formatted_title = title[:20].strip()
            formatted_status_code = str(status_code).strip()
            formatted_url = url.strip()

            lock.acquire()
            if status_code < 404:
                print(Fore.LIGHTRED_EX + f"  {formatted_status_code.center(5)}   " +
                      Fore.LIGHTBLUE_EX + f" {formatted_url.ljust(40)}" + Fore.LIGHTGREEN_EX + f"{formatted_title.center(20)}")
            else:
                print(Fore.YELLOW + f"  {formatted_status_code.center(5)}   " +
                      Fore.LIGHTBLUE_EX + f" {formatted_url.ljust(40)}" + Fore.LIGHTGREEN_EX + f"{formatted_title.center(20)}")
            print('进度:{:.2%} \t进度条不太准，但也大差不差'.format(n / urls_len), end='\r', flush=True)
            lock.release()

            return (status_code, formatted_url, formatted_title)
    except:
        lock.acquire()
        exception_counter += 1
        lock.release()

    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", required=True, help="传入一个文件")
    parser.add_argument("-t", type=int, default=50, help="线程数，默认为50")
    parser.add_argument("-x", default="", help="需要排除的状态码，多个状态码通过逗号分隔")
    args = parser.parse_args()
    n = 0
    if not args.f.endswith(".txt"):
        print("必须使用txt文件！")
        return

    exclude_codes = set(map(int, args.x.split(','))) if args.x else set()
    threads = args.t

    file_dir = os.path.dirname(args.f)
    output_file = os.path.join(file_dir, "web存活.csv")

    with open(args.f, "r") as file:
        urls = [line.strip() for line in file.readlines()]
        urls_len = len(urls)

    alive_urls = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for url in urls:
            n += 1
            future = executor.submit(check_url, url, exclude_codes, n, urls_len)
            futures.append(future)

        for future in as_completed(futures):
            result = future.result()
            if result:
                alive_urls.append(result)

    progress = (n - exception_counter) / urls_len
    print('进度:{:.2%} '.format(progress), end='\r', flush=True)

    alive_urls.sort()  # 按照状态码排序

    with open(output_file, "w", encoding="utf-8", newline='') as output:
        writer = csv.writer(output)
        writer.writerow(["code", "URL", "title"])
        writer.writerows(alive_urls)

    progress_bar = '进度: {:.2%} '.format(n / urls_len)
    if n == urls_len:
        progress_bar += '\n'
    print(progress_bar, end='\r', flush=True)


if __name__ == "__main__":
    os.system("cls")
    print("")
    print(Fore.LIGHTYELLOW_EX + "在命令框中:\n\turl仅能显示40字节，\n\ttitle显示20字节，\n如若不全，请到传入文件的同目录下查看web存活.csv文件\n\turl显示70字节\ttitle显示40字节\t不够的去urlbatch.py的97，98行将数值增大即可")
    print("\n")
    x_status_code = "code".center(7, ' ')
    x_URL = "URL".center(40, ' ')
    x_Title = "title".center(20, ' ')
    print(Fore.LIGHTRED_EX + f"{x_status_code}" + Fore.LIGHTGREEN_EX + f"{x_URL}" + Fore.LIGHTBLUE_EX + f"{x_Title}")
    columns, _ = shutil.get_terminal_size()
    print('_' * int(columns))
    main()
    print('')
    print(Fore.LIGHTMAGENTA_EX + "程序结束，拜拜")

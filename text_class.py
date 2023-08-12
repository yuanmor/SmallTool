import os
import argparse

extensions = [
    '3ds', 'aac', 'ai', 'aif', 'aiff', 'amr', 'apk', 'app', 'arw', 'asf', 'asp', 'avi', 'bak', 'bat',
    'bin', 'bmp', 'bz2', 'c',
    'class', 'com', 'conf', 'cpp', 'css', 'csv', 'dat', 'deb', 'dll', 'doc', 'docx', 'dmg', 'djvu', 'dot',
    'dotx', 'dwg', 'dxf',
    'eps', 'exe', 'flac', 'flv', 'gif', 'gz', 'h', 'htm', 'html', 'ico', 'ini', 'ipa', 'iso', 'jar',
    'java', 'jpeg', 'jpg',
    'js', 'json', 'log', 'm4a', 'm4v', 'mkv', 'mov', 'mp3', 'mp4', 'mpeg', 'mpg', 'msi', 'odb', 'odf',
    'odg', 'ods', 'odt',
    'ogg', 'ogv', 'otf', 'pdb', 'pdf', 'php', 'pl', 'png', 'ppt', 'pptx', 'psd', 'py', 'rar', 'rb',
    'rtf', 'sh', 'sql',
    'svg', 'swf', 'tar', 'tif', 'tiff', 'tmp', 'ttf', 'txt', 'wav', 'webm', 'webp', 'wma', 'wmv', 'xls',
    'xlsx', 'xml', 'xps',
    'yaml', 'yml', 'zip', 'asp', 'aspx', 'jsp', 'jspx', 'mdb', 'zip', 'rar', 'tar', '7z', 'bak', 'gif', 'dll', 'sql',
    'as', 'swf',
    'exe', 'ini', 'jpg', 'net', 'jpeg', 'png', 'aaa', 'pack', 'cfm', 'cgi', 'icn', 'doc', 'csv', 'csvx',
    'xls', 'xlsx', 'pdf',
    'ppt', 'cer', 'do', 'sh', 'test', 'upload', 'wml',
    'c', 'h', 'cpp', 'hpp', 'cc', 'hh', 'cxx', 'hxx', 'java', 'jar', 'py',
    'pyc', 'pyd', 'pyo', 'pyw', 'js', 'php', 'php3', 'php4', 'php5', 'phtml',
    'html', 'htm', 'css', 'go', 'sh',
    'bash', 'zsh','inc','asa','aspxx','ashx','ascx',''
]
encoding = "utf-8"


def main():
    parser = argparse.ArgumentParser(description="Split lines from a text file based on file extensions")
    parser.add_argument("-f", "--file", help="Input text file path")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Number of threads")
    args = parser.parse_args()
    directory = os.path.dirname(args.file)
    with open(args.file, 'r', errors='ignore') as f:
        lines = f.readlines()

    for line in lines:
        if "." in line:
            n = line.rfind(".") + 1
            ext = line[n:].strip().lower()
            if ext in extensions:
                output_file = os.path.join(directory, "{}.txt".format(ext))
            else:
                output_file = os.path.join(directory, "path.txt")
        else:
            output_file = os.path.join(directory, "path.txt")

        with open(output_file, "a+", encoding=encoding) as f:
            f.write(line)

    print("执行完毕")
if __name__ == "__main__":
    main()

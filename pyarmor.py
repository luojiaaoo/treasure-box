'''
@Project : treasure-box 
@File    : pyarmor.py
@Author  : luojiaaoo
@Page    : https://github.com/luojiaaoo
@Link    : https://github.com/luojiaaoo/treasure-box
'''

import argparse
import os
import re
from pathlib import Path
import subprocess
import shutil

root_dir_path = Path(__file__).parent
# 路径切换到项目路径
os.chdir(root_dir_path.__str__())
# 切换到有pyarmor的python环境
os.environ["PATH"] = (
    f"{(root_dir_path / 'plugins' / 'run' / 'python-x64').__str__()};{(root_dir_path / 'plugins' / 'run' / 'python-x64' / 'Scripts').__str__()};"
    + os.environ["PATH"]
)
parser = argparse.ArgumentParser(description="run pyarmor")
# 需要加密的python文件夹路径（库）
parser.add_argument("-p", "--packages", dest="packages", nargs="?", help="Enter packages")
# 需要加密的单文件
parser.add_argument("-f", "--pyfiles", dest="pyfiles", nargs="?", help="Enter pyfile")
args = parser.parse_args()
list_package = (
    [os.path.abspath(i) for i in args.packages.replace(" ", "").split(",")] if args.packages else []
)
list_pyfile = [os.path.abspath(i) for i in args.pyfiles.replace(" ", "").split(",")] if args.pyfiles else []

# 需要加密的代码剪切到临时文件夹
temp_dir_path = root_dir_path / "temp_pyarmor"
if os.path.exists(temp_dir_path.__str__()):
    shutil.rmtree(temp_dir_path.__str__())
os.mkdir(temp_dir_path.__str__())
for pyfile_ in list_pyfile:
    shutil.move(pyfile_, (temp_dir_path / os.path.basename(pyfile_)).__str__())
for package_ in list_package:
    shutil.move(package_, (temp_dir_path / os.path.basename(package_)).__str__())

# 运行加密脚本，把加密python放回原处
exe_pyarmor_file_path = (root_dir_path / "plugins" / "run" / "python-x64" / "Scripts" / "pyarmor").__str__()
for pyfile_ in list_pyfile:
    subprocess.call(
        [
            exe_pyarmor_file_path,
            "gen",
            "--output",
            os.path.dirname(pyfile_),
            (temp_dir_path / os.path.basename(pyfile_)).__str__(),
        ]
    )
for package_ in list_package:
    subprocess.call(
        [
            exe_pyarmor_file_path,
            "gen",
            "--output",
            os.path.dirname(package_),
            "-r",
            "-i",
            (temp_dir_path / os.path.basename(package_)).__str__(),
        ]
    )


# 保留import记录以供pyinstaller检测依赖
def normal_import(list_import):
    list_import = [re.sub("\s+", " ", i).strip() for i in list_import]
    list_import = [re.sub("#.+", "", i).strip() + "\n" for i in list_import]
    list_import = list(set(list_import))
    return list_import


list_import_all = []
for pyfile_ in list_pyfile:
    with open((temp_dir_path / os.path.basename(pyfile_)).__str__(), "r", encoding="utf-8") as f:
        list_import_all.extend([i for i in f.readlines() if re.match(r".*\s*import\s+.+", i)])
for package_ in list_package:
    files = (
        os.path.join(root, name)
        for root, dirs, files in os.walk((temp_dir_path / os.path.basename(package_)).__str__())
        for name in files
        if name.endswith(".py")
    )
    for file_ in files:
        with open(file_, "r", encoding="utf-8") as f:
            list_import_all.extend([i for i in f.readlines() if re.match(r".*\s*import\s+.+", i)])
list_import_all = normal_import(list_import_all)
with open("impoort_for_pyarmor.py", "w", encoding="utf-8") as f:
    f.writelines(list_import_all)

# 运行打包脚本
subprocess.call([(root_dir_path / "scripts" / "runPyinstaller.bat").__str__()])

# 还原代码文件
for pyfile_ in list_pyfile:
    os.remove(pyfile_)
    shutil.move((temp_dir_path / os.path.basename(pyfile_)).__str__(), pyfile_)
for package_ in list_package:
    shutil.rmtree(package_)
    shutil.move((temp_dir_path / os.path.basename(package_)).__str__(), package_)

# 删除临时文件
temp_dirs = (
    os.path.join(root, dir_)
    for root, dirs, files in os.walk(root_dir_path.__str__())
    for dir_ in dirs
    if dir_ == "pyarmor_runtime_000000"
)
for temp_dir in temp_dirs:
    shutil.rmtree(temp_dir)
os.remove("impoort_for_pyarmor.py")

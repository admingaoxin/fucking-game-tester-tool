import os

from thread import Settings

import handelexcel
def svn_checkout():
    """
    co 配置文件
    :return:
    """
    cmd_co = "svn -r HEAD checkout %(url)s %(dist)s --username %(username)s --password %(password)s" % Setting.setting
    cmd_up = "svn up"
    if not os.path.exists(Settings.setting["dist"]):
        os.system(cmd_co)
    os.system(cmd_up)
 
def svn_up_to_rev(rev, filepaths):
    """
    更新到某一版本
    :return:
    """
    if filepaths is not None:
        cmd_up = "svn up -r %s %s" % (rev, filepaths)
        print("执行更新版本：%s" %rev)
        os.system(cmd_up)
 
def svn_get_info(rev, filenames, fieldnames, side):
    """
    获取svn信息
    cmd = svn log -v -r rev
    :return:value_list
    """
    file_list=[]
    if "," in filenames:
        file_list = "".join(filenames).split(",")
    else:
        file_list.append(filenames)
    files_dict = {}
    value_list = []
    svn_checkout()
    os.chdir(Setting.setting["dist"])
    for root, dirs, files in os.walk(Setting.setting["dist"]):
        for file in files:
            if file.endswith(".xlsx") or file.endswith(".xls"):
                _file = file.split(".")[0]
                files_dict[_file] = os.path.relpath(os.path.join(root, file), Setting.setting["dist"])
    for filename in file_list:
        if filename not in list(files_dict.keys()):
            print("输入的文件不存在！请确认文件名是否正确！")
            continue
        svn_up_to_rev(rev, files_dict[filename])
        info_cmd = "svn log -v -r %s %s" % (rev, files_dict[filename])
        svn_info = "".join(os.popen(info_cmd).readlines())
        if "Changed paths:" in svn_info:
            docs = svn_info.split("Changed paths:")[1].split("--")[0].strip().split("\n")
            for doc in docs:
                if any(st in doc for st in ("M /", "A /")) and any((doc.endswith(".xls"), doc.endswith(".xlsx"))):
                    file = doc.strip().split(" /")[1]
                    value_dict = HandleExcels.parse_excel(file, fieldnames, side)
                    value_list.append(value_dict)
                    return value_list
                else:
                    pass
        else:
            file_cmd = "svn log -v -r  %s" % (files_dict[filename])
            svn_rev_info = os.popen(file_cmd).readlines()
            rev_list = []
            for info in svn_rev_info:
                if " | " in info:
                    ve = "".join(re.findall("\d+", info.split(" | ")[0]))
                    rev_list.append(ve)
            rev_list.sort()
            last_list = []
            for _rev in rev_list:
                if int(_rev) < int(rev):
                    last_list.append(int(_rev))
            last_list.sort()
            last_rev = last_list[-1]
            svn_up_to_rev(last_rev, files_dict[filename])
            value_dict = HandleExcels.parse_excel(files_dict[filename], fieldnames, side)
            value_list.append(value_dict)
            # print("value_list",value_list)
    return value_list
 
def get_files(rev, parameters):
    """
    获取文件路径
    :return:
    """
    file_list = svn_get_info(rev, parameters)
    root = os.getcwd()
    file_paths = []
    for file in file_list:
        path = os.path.join(root, file)
        _file_path = path.replace("\\", "/")
        file_paths.append(_file_path)
    print(file_paths)
    return file_paths
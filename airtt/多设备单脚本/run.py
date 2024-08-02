
import os
import jenkinsfile
print("当前工作目录:", os.getcwd())
import sys
import os
import traceback
import subprocess
import webbrowser
import time
import json
import shutil
from airtest.core.android.adb import ADB
from jinja2 import Environment, FileSystemLoader
import datetime
from jenkinsfile import dev,air
""""
##这一段是给jenkins环境下找不到自己二次封装的包用的
# 
# rootpath=str("C:\\Users\\cm619\\.jenkins\\workspace\\RPAdemo")
# syspath=sys.path
# sys.path=[]
# sys.path.append(rootpath)#将工程根目录加入到python搜索路径中
# sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
# sys.path.extend(syspath)
"""

#暂时不考虑性能，走全局变量

Nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
reprot_file = f"D:\\qatoolswc\\airtt\\report_file\\{Nowtime}"



def run(devices, air, run_all = True):
    """"
        run_all
            = True: 从头开始完整测试 (run test fully) ;
            = False: 续着data.json的进度继续测试 (continue test with the progress in data.jason)
    """
    try:
        results = load_jdon_data(air, run_all)
        tasks = run_on_multi_device(devices, air, results, run_all,dev)
        for task in tasks:
            status = task['process'].wait()
            results['tests'][task['dev']] = run_one_report(task['air'], task['dev'])
            results['tests'][task['dev']]['status'] = status
            json.dump(results, open('data.json', "w"), indent=4)
        run_summary(results)
    except Exception as e:
        traceback.print_exc()


def run_on_multi_device(devices, air, results, run_all,dev):
    """
        在多台设备上运行airtest脚本
    """
    tasks = []

    if dev in devices:
        print (dev)
        if (not run_all and results['tests'].get (dev) and
            results['tests'].get (dev).get ('status') == 0):
                print ("Skip device %s" % dev)
    elif dev == 'ALL' :
        for devs in devices:
            dev = devs
            print(dev)
            if (not run_all and results['tests'].get(dev) and
               results['tests'].get(dev).get('status') == 0):
                print("Skip device %s" % dev)
                continue

    log_dir = get_log_dir(dev, air)
    cmd = [
        "airtest",
        "run",
        air,
        "--device",
        "Android:///" + dev,
        "--log",
        log_dir
    ]
    try:
        tasks.append({
            'process': subprocess.Popen(cmd, cwd=os.getcwd()),
            'dev': dev,
            'air': air
        })
    except Exception as e:
        traceback.print_exc()
    return tasks


def run_one_report(air, dev):
    """"
        生成一个脚本的测试报告
    """

    # airname
    airname = air.replace('.air', '')

    try:
        log_dir = get_log_dir(dev, air)
        log = os.path.join(log_dir,f'log.txt')
        if os.path.isfile(log):
            cmd = [
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--lang",
                "zh",
                "--export",
                log_dir #, f'{Nowtime}{dev}.html'
            ]
            ret = subprocess.call(cmd, shell=True, cwd=os.getcwd())
            return {
                    'status': ret,
                    'path': os.path.join(log_dir, f'{airname}.log\\log.html')
                    }
        else:
            print("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc()
    return {'status': -1, 'device': dev, 'path': ''}


def run_summary(data):
    """"
        生成汇总的测试报告
    """
    try:
        summary = {
            'time': "%.3f" % (time.time() - data['start']),
            'success': [item['status'] for item in data['tests'].values()].count(0),
            'count': len(data['tests'])
        }
        summary.update(data)
        summary['start'] = time.strftime("%Y-%m-%d %H:%M:%S",
                                         time.localtime(data['start']))
        env = Environment(loader=FileSystemLoader(os.getcwd()),
                          trim_blocks=True)
        html = env.get_template('report_tpl.html').render(data=summary)
        with open(f"{Nowtime}{dev}-report.html", "w", encoding="utf-8") as f:
            f.write(html)
        # webbrowser.open(f'log.html')
    except Exception as e:
        traceback.print_exc()

    # cat_report_date(air)

def load_jdon_data(air, run_all):
    """"
        加载进度
            如果data.json存在且run_all=False，加载进度
            否则，返回一个空的进度数据
    """
    json_file = os.path.join(os.getcwd(), 'data.json')
    if (not run_all) and os.path.isfile(json_file):
        data = json.load(open(json_file))
        data['start'] = time.time()
        return data
    else:
        print('不清除log文件夹')
        # clear_log_dir(air)
        return {
            'start': time.time(),
            'script': air,
            'tests': {}

        }

# def cat_report_date(air):
#     """
#     试试能不能移动文件到一个固定的报告文件夹
#     """
#     log = os.path.join (os.getcwd (), air, 'log')
#     if os.path.exists (log):
#         shutil.copytree(log, reprot_file)
#         # # 复制文件夹中的所有文件到目标文件夹
#         # for root, dirs, files in os.walk (log):
#         #     for file in files:
#         #         src_file = os.path.join (root, file)
#         #         dst_file = os.path.join (reprot_file, file)
#         #         shutil.copy2 (src_file, dst_file)


def clear_log_dir(air):
    """"
        清理log文件夹
    """
    log = os.path.join(os.getcwd(), air, 'log')
    if os.path.exists(log):
        shutil.rmtree(log)


def get_log_dir(device, air):
    """"
         文件夹下创建每台设备的运行日志文件夹
    """
    devicesa = str(device+Nowtime)
    log_dir = os.path.join(air, 'log', devicesa.replace(".", "_").replace(':', '_'))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir


if __name__ == '__main__':
    """
        初始化数据
    """
    devices = [tmp[0] for tmp in ADB().devices()]
    # air = 'try.air'


    # 基于data.json的进度，跳过已运行成功的脚本
    # run(devices, air)
    # 重新运行所有脚本
    run(devices, air, run_all=True)

import os

print ("当前工作目录:", os.getcwd ())
import sys
from pathlib import Path

sys.path.append (str (Path (__file__).resolve ().parents[1]))
import traceback
import subprocess
import webbrowser
import time
import json
import shutil
from airtest.core.android.adb import ADB
from jinja2 import Environment, FileSystemLoader
import datetime
from config import jenkinsfile

""""
##这一段是给jenkins环境下找不到自己二次封装的包用的
"""

# rootpath=str("C:\\Users\\cm619\\.jenkins\\workspace\\test\\casefile")
# syspath=sys.path
# sys.path=[]
# sys.path.append(rootpath)#将工程根目录加入到python搜索路径中
# sys.path.extend([rootpath+i for i in os.listdir(rootpath) if i[0]!="."])#将工程目录下的一级目录添加到python搜索路径中
# sys.path.extend(syspath)


# 暂时不考虑性能，走全局变量

Nowtime = datetime.datetime.now ().strftime ("%Y-%m-%d-%H-%M-%S")
report_file = f"C:\\Users\\cm619\\.jenkins\\workspace\\test\\report"


def run(devices, airs, run_all=True):
    """
        run_all
            = True: 从头开始完整测试 (run test fully);
            = False: 续着data.json的进度继续测试 (continue test with the progress in data.json)
    """
    try:
        all_results = []
        for air in airs:
            results = load_jdon_data (air, run_all)
            tasks = run_on_multi_device (devices, air, dev, results, run_all)
            for task in tasks:
                status = task['process'].wait ()
                results['tests'][task['dev']] = run_one_report (task['air'], task['dev'])
                results['tests'][task['dev']]['status'] = status
                json.dump (results, open ('data.json', "w"), indent=4)
            all_results.append (results)
            run_summary (results, air)
        generate_overall_report (all_results)
    except Exception as e:
        traceback.print_exc ()


def run_on_multi_device(devices, air, dev, results, run_all):
    """
        在多台设备上运行airtest脚本
    """
    tasks = []
    if dev == 'ALL':
        for dev in devices:
            print (dev)
            if (not run_all and results['tests'].get (dev) and
                    results['tests'].get (dev).get ('status') == 0):
                print ("Skip device %s" % dev)
                continue

            log_dir = get_log_dir (dev, air)
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
                tasks.append ({
                    'process': subprocess.Popen (cmd, cwd=os.getcwd ()),
                    'dev': dev,
                    'air': air
                })
            except Exception as e:
                traceback.print_exc ()
    else:
        # 如果不是'ALL'，则只处理指定的设备
        print (dev)
        if dev in devices:
            if (not run_all and results['tests'].get (dev) and
                    results['tests'].get (dev).get ('status') == 0):
                print ("Skip device %s" % dev)
                return tasks  # 直接返回空任务列表

            log_dir = get_log_dir (dev, air)
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
                tasks.append ({
                    'process': subprocess.Popen (cmd, cwd=os.getcwd ()),
                    'dev': dev,
                    'air': air
                })
            except Exception as e:
                traceback.print_exc ()
    return tasks


def run_summary(data, air):
    """"
        生成汇总的测试报告
    """
    try:
        summary = {
            'time': "%.3f" % (time.time () - data['start']),
            'success': [item['status'] for item in data['tests'].values ()].count (0),
            'count': len (data['tests'])
        }
        summary.update (data)
        summary['start'] = time.strftime ("%Y-%m-%d %H:%M:%S", time.localtime (data['start']))
        env = Environment (loader=FileSystemLoader (os.getcwd ()), trim_blocks=True)
        html = env.get_template ('report_tpl.html').render (data=summary)
        report_path = f"report\\{air}\\{Nowtime}_{air.replace ('.air', '')}-report.html"
        with open (report_path, "w", encoding="utf-8") as f:
            f.write (html)
        print (f"Report generated: {report_path}")
        # webbrowser.open(f'log.html')
    except Exception as e:
        traceback.print_exc ()

    # cat_report_date(air)


def generate_overall_report(all_results):
    try:
        total_scripts = len (all_results)
        total_success = sum ([result.get ('success', 0) for result in all_results])
        total_tests = sum ([result.get ('count', 0) for result in all_results])

        html_content = f"""
        <html>
        <head>
            <title>汇总测试报告</title>
            <style>
                body {{
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                }}
                .container {{
                    border: 1px solid #ccc;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 80%;
                    max-width: 800px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                h1 {{
                    text-align: center;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>汇总测试报告</h1>
                <p>总用例数: {total_scripts}</p>
                <p>成功数: {total_success}</p>

                <table>
                    <tr>
                        <th>Script</th>
                        <th>Success Rate</th>
                        <th>Report Link</th>
                    </tr>
        """

        for result in all_results:
            script = result['script']
            success_count = [item['status'] for item in result['tests'].values ()].count (0)  # 假设0表示成功
            total_count = len (result['tests'])
            success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
            report_path = f"{script}\\{Nowtime}_{script.replace ('.air', '')}-report.html"  # 注意：这里假设Nowtime和report_file已定义

            # 如果成功率为100%，则增加总成功数
            if success_rate == 100:
                total_success += 1

            # 更新总测试数（如果需要）
            total_tests += total_count

            html_content += f"""
            <tr>
                <td>{script}</td>
                <td>{success_rate:.2f}%</td>
                <td><a href="{report_path}">View Report</a></td>
            </tr>
            """

        # 在HTML中更新成功数
        html_content = html_content.replace ('成功数: 0', f'成功数: {total_success}', 1)

        html_content += """
            </table>

        </body>
        </html>
        """
        #            # <p>Total Tests: {total_tests}</p> {# 如果需要显示总测试数 #}
        overall_report_path = f"{report_file}\\{Nowtime}overall_report.html"
        with open (overall_report_path, "w", encoding="utf-8") as f:
            f.write (html_content)
        print (f"Overall report generated: {overall_report_path}")
        # webbrowser.open(overall_report_path)  # 如果需要自动打开报告，取消注释这行代码
    except Exception as e:
        traceback.print_exc ()


def load_jdon_data(air, run_all):
    """"
        加载进度
            如果data.json存在且run_all=False，加载进度
            否则，返回一个空的进度数据
    """
    json_file = os.path.join (os.getcwd (), 'data.json')
    if (not run_all) and os.path.isfile (json_file):
        data = json.load (open (json_file))
        data['start'] = time.time ()
        return data
    else:
        print ('不清除log文件夹')
        # clear_log_dir(air)
        return {
            'start': time.time (),
            'script': air,
            'tests': {}

        }


def run_one_report(air, dev):
    """"
        生成一个脚本的测试报告
    """
    # os.chdir(air)
    airname = air.replace ('.air', '')
    report_file_log = f"{report_file}\\{air}\\log\\{dev}{Nowtime}"
    print ('report_file_log', report_file_log)
    report_file_logs = report_file_log.replace (f"{report_file}\\{air}\\", '')
    print ('report_file_logs', report_file_logs)
    try:
        log_dir = get_log_dir (dev, air)
        log = os.path.join (log_dir, f'log.txt')

        if os.path.isfile (log):
            cmd = [
                "airtest",
                "report",
                air,
                "--log_root",
                log_dir,
                "--lang",
                "zh",
                "--export",
                report_file_log  # , f'{Nowtime}{dev}.htmllog_dir'
            ]
            ret = subprocess.call (cmd, shell=True, cwd=os.getcwd ())
            # os.chdir(workspace_file)
            return {
                'status': ret,
                'path': os.path.join (report_file_logs, f'{airname}.log\\log.html')
            }

        else:
            print ("Report build Failed. File not found in dir %s" % log)
    except Exception as e:
        traceback.print_exc ()
    return {'status': -1, 'device': dev, 'path': ''}


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
    log = os.path.join (os.getcwd (), air, 'log')
    if os.path.exists (log):
        shutil.rmtree (log)


def get_log_dir(device, air):
    """
         文件夹下创建每台设备的运行日志文件夹
    """
    devicesa = str (device + Nowtime)
    # report = str('{report_file}\\report'+air)
    log_dir = os.path.join (air, 'log', devicesa.replace (".", "_").replace (':', '_'))
    # log_dir = f"C:\\Users\\cm619\\.jenkins\\workspace\\test\\{air}\\log\\{devicesa.replace('.', '_').replace(':', '_')}"
    if not os.path.exists (log_dir):
        os.makedirs (log_dir)
    return log_dir


if __name__ == '__main__':
    """
        初始化数据
    """
    devices = [tmp[0] for tmp in ADB ().devices ()]
    # air = 'try.air'
    airs = jenkinsfile.airs
    dev = jenkinsfile.dev
    print (airs, dev)
    # 基于data.json的进度，跳过已运行成功的脚本
    # run(devices, air)
    # 重新运行所有脚本
    run (devices, airs, run_all=True)

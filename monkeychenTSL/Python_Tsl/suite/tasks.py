import shutil
import subprocess
import sys
import time
from pathlib import Path
import os

from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tesla.settings')
current_dir = Path(__file__)

TSL_work_path = settings.BASE_DIR / settings.TSL_WORK
python_path = sys.executable

test_path = [  # N个不同的用例目录
    TSL_work_path / "tests/bbs",
    TSL_work_path / "tests/beifan",
    TSL_work_path / "tests/ddt",
]

run_path = TSL_work_path / "main_by_django.py"
case_path = TSL_work_path / "tests/test_case.py"
ini_path = TSL_work_path / "pytest.ini"


def run_pytest(path, result_id=0, case_api_count=0):
    print("开始创建进程启动框架", time.time())
    if case_api_count > 0:
        # 有接口测试用例
        cmd = f"{python_path} {run_path} -c {ini_path} {case_path} ./ result_id {result_id}"
    else:
        # 无接口测试用例
        cmd = f"{python_path} {run_path} -c {ini_path}  ./ result_id {result_id}"
    cmd = cmd.split(" ")
    print("cmd",cmd)
    process = subprocess.run(
        cmd,
        cwd=path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )  # 创建子进程
    # 编码 和 解密  要一致
    # print(process)

    try:
        print(process.stdout.decode("utf-8"))
        print(process.stderr.decode("utf-8"))
    except UnicodeDecodeError:
        print("try gbk")
        print(process.stdout.decode("gbk"))
        print(process.stderr.decode("gbk"))
    shutil.make_archive(f"artifacts_{result_id}", "zip", path)
    shutil.move(f"artifacts_{result_id}.zip", Path(path) / "artifacts.zip")



def run_by_cron(suite_id):
    from .models import Suite

    suite: Suite = Suite.objects.get(id=suite_id)
    return suite.run()


def _test_task():
    from .models import Suite

    c = Suite.objects.all().count()
    print("测试套件数量", c)
    return c


#
# if __name__ == "__main__":
#     pool = ThreadPoolExecutor(max_workers=4)  # 8-2
#     pool.map(run_pytest, [r"D:\Python_Tsl\Temporary_storage"])
#     pool.shutdown()
#     print("end")
if __name__ == "__main__":
    print(settings)

import os
import shlex
import sys  # 和python内部打交道
from pathlib import Path

import pytest
from django import setup
print("main_by_django文件")

result_id = sys.argv[-1]
sys.argv = sys.argv[:-2]
path = Path(__file__).parents[1]  # 上级目录
sys.path.append(str(path))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tesla.settings")
setup()

from suite.models import RunResult

result: RunResult = RunResult.objects.get(id=result_id)

result.status = result.RunStatus.Running
result.save()
ret_code = pytest.main()  # 启动框架，得到结果


# sys.exit(-1)
if ret_code == pytest.ExitCode.OK:
    print("测试通过")
    result.is_pass = True
    result.save()
else:
    print("测试失败")

result.status = result.RunStatus.Reporting
result.save()

command = "allure generate -o report temps --clean"
args = shlex.split(command)
ret_code = os.system(" ".join(args))
print("ret_code",ret_code)

if ret_code == pytest.ExitCode.OK:
    print("报告生成成功")
    result.status = result.RunStatus.Done
    result.save()
else:
    print("报告生成失败")
    result.status = result.RunStatus.Error
    result.save()

result: RunResult = RunResult.objects.get(id=result_id)
print(result_id, result.is_pass, result.status)
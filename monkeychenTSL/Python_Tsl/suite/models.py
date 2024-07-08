import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from django.db import models
from django_q.humanhash import uuid
from django_q.models import Schedule
from django_q.tasks import schedule

from case_api.models import Case as CaseAPI
from case_ui.models import Case as CaseUI
from project.models import Project
from suite.tasks import run_pytest


class Suite(models.Model):
    """测试套件"""

    objects: models.QuerySet

    class RunType(models.TextChoices):
        ONCE = "O", "单次执行"
        CRON = "C", "Cron"
        WebHook = "W", "WebHook"

    name = models.CharField("套件名称", max_length=32)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField("套件描述", max_length=250, blank=True)

    case_ui_list = models.ManyToManyField(CaseUI, blank=True)
    case_api_list = models.ManyToManyField(CaseAPI, blank=True)

    run_type = models.CharField(
        "运行类型", choices=RunType.choices, default=RunType.ONCE, max_length=1
    )

    cron = models.CharField("cron表达式", max_length=20, blank=True)
    hook_key = models.CharField("hook密钥", max_length=255, blank=True)

    schedule = models.ForeignKey(Schedule, null=True, blank=True,on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        # 创建调度任务
        if self.run_type == self.RunType.CRON:
            self.schedule = schedule(
                "suite.tasks.run_by_cron", self.id, cron=self.cron, schedule_type="C"
            )
        else:
            if self.schedule:  # 如果不再是定时执行，就删除调度任务
                self.schedule.delete()
                self.schedule = None
        if self.run_type == self.RunType.WebHook:
            # 创建WebHook的秘钥
            if not self.hook_key:
                self.hook_key = uuid()[0]

        return super().save(*args, **kwargs)

    def case_ui_count(self):
        """UI用例数量"""
        return self.case_ui_list.all().count()

    def case_api_count(self):
        """api用例数量"""
        return self.case_api_list.all().count()

    def run(self):
        """执行套件中的用例"""
        # 1.生成执行结果
        # 2.生成yaml和excl测试用例
        # 3.子进程
        #  1.启动pytest
        #  2.更新执行结果

        # 1.生成执行结果
        result: RunResult = RunResult.objects.create(
            suite=self, project=self.project, path="todo"
        )

        path = Path("upload_yaml") / f"result_{result.id}_{time.time()}"  # 创建绝不重名的目录名
        path.mkdir(parents=True, exist_ok=True)  # 创建目录
        result.path = path
        result.save()

        # 2.生成yaml和excl测试用例
        case_api: CaseAPI
        for case_api in self.case_api_list.all():
            case_api.to_yaml(path)
        case_ui: CaseUI
        for case_ui in self.case_ui_list.all():
            case_ui.to_xlsx(path)

        # 3.子进程
        #  1.启动pytest
        #  2.更新执行结果
        pool = ThreadPoolExecutor(max_workers=4)  # 8-2
        pool.submit(run_pytest, path, result.id, self.case_api_count())
        return result


class RunResult(models.Model):
    """执行结果"""

    objects: models.QuerySet

    class RunStatus(models.IntegerChoices):
        Init = 0, "初始化"
        Ready = 1, "准备开始"
        Running = 2, "正在执行"
        Reporting = 3, "正在正常报告"
        Done = 4, "执行完毕"
        Error = -1, "执行出错"

    suite = models.ForeignKey(Suite, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    path = models.CharField("用例路径", max_length=255)
    is_pass = models.BooleanField("测试通过", default=False)

    status = models.IntegerField(
        "执行状态", choices=RunStatus.choices, default=RunStatus.Init
    )

    create_datetime = models.DateTimeField("创建时间", auto_now_add=True)
    update_datetime = models.DateTimeField("更新时间", auto_now=True)

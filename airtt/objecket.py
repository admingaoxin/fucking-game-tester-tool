import time
from venv import logger
from airtest.core.api import touch as old_touch, snapshot
from airtest.core.error import TargetNotFoundError
from airtest.core.api import wait as old_wait
from airtest.core.helper import logwrap
from airtest.core.cv import Template, loop_find, try_log_screen
from airtest.core.api import touch as old_touch, snapshot

@logwrap
def touch(target, v, timeout=20,retry_interval=1, **kwargs):
    starttime = time.time()

    while True:
        try:
            old_touch(target)
            pos = v
            return pos
        except TargetNotFoundError:
            curent_time = time.time()
            elpased_time = time.time() - starttime

            if elpased_time > timeout:
                #超时了，就捕获异常并记录一下
                logger.error(f"在指定的时间{timeout}内没找到图片")
                snapshot(filename=f"error_{curent_time}.png")
                raise
            else:
                logger.error(f"没找到图片，{retry_interval}秒内重试")
                time.sleep(retry_interval)
                continue
        except Exception as e:
            curent_time = time.time()
            logger.error(f"点击图片时发生未知错误：{e}")


@logwrap
def wait(v, timeout=20, interval=0.5,intervalfunc=None, **kwargs):
    starttime = time.time()
    while True:
        try:
            old_wait(v)
            logger.info(f"等到了要找的图")
            break
        except TargetNotFoundError:
            curent_time = time.time()
            elpased_time = time.time() - starttime

        if elpased_time > timeout:
            # 超时了，就捕获异常并记录一下
            logger.error (f"在指定的时间{timeout}S内没找到图片")
            snapshot(filename=f"error_Notfound{curent_time}.png")
            raise TargetNotFoundError('Picture %s not found in screen')


# @logwrap
# def exists(v,timeout=30):
#     starttime = time.time()
#     while True:
#         try:
#             old_exists(v)
#             return v
#             logger.info('终于等到你')
#             break
#         except TargetNotFoundError:
#             snapshot(filename=f"error_没找到要找的图.png")
#             logger.error("没等到这张图，无法继续下一步操作")
#         if time.time() - starttime > timeout:
#             print(f'超时了一直没找到{v}')


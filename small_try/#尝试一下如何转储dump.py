import os
import ctypes
from ctypes import wintypes
import win32con
import psutil
proc_name = "SYNCED.exe"
# 获取所有进程信息
for proc in psutil.process_iter():
    try:
        if proc.name() == proc_name:
            pid = proc.pid  # 如果名称匹配，则获取该进程ID
            print("进程名称: ", proc_name, "PID: ", pid)
        # else : 
        #     print("找不到进程")
            
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass
    #     pinfo = proc.as_dict(attrs=['pid', 'name'])

    #     # 打印进程PID和名称
    #     print(pinfo['pid'], pinfo['name'])
    # except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
    #     pass
# 打开进程 SYNCED-Win64-Development.exe
PROCESS_ALL_ACCESS = 0x1F0FFF
process_id = pid
print(process_id)
# process_id = 30440  # 替换为你要转储的进程ID
kernel32_dll = ctypes.WinDLL('kernel32', use_last_error=True)
process_handle = kernel32_dll.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)

# 使用miniDumpWriteDump函数进行转储操作
dbghelp_dll = ctypes.WinDLL('Dbghelp.dll', use_last_error=True)
filename = 'synced.dmp'  # 转储文件的名称
handle = kernel32_dll.CreateFileW(
    filename,
    0x10000000,  # GENERIC_WRITE
    0,
    None,
    2,  # CREATE_ALWAYS
    0,
    None
)
MINIDUMP_TYPE = ctypes.c_int
MiniDumpWithFullMemory = 2
dump_flags = MINIDUMP_TYPE(MiniDumpWithFullMemory)
dbghelp_dll.MiniDumpWriteDump(
    process_handle,
    process_id,
    handle,
    dump_flags,
    None,
    None,
    None
)

# 关闭相关句柄和资源
kernel32_dll.CloseHandle(handle)
kernel32_dll.CloseHandle(process_handle)
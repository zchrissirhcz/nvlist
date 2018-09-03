#!/usr/bin/env python
#coding: utf-8

"""
Author: Zhuo Zhang

Description:
    This script is an alternate to `nvidia-smi`.
    It provides process's username, and removes items such as GPU Fan, Perf, etc

Dependencies:
    sudo pip install nvidia-ml-py
"""

from __future__ import print_function
import pynvml as pml
import psutil

pml.nvmlInit()

# 显卡数量
deviceCount = pml.nvmlDeviceGetCount()

mega = 1024 * 1024

"""
gpu_id gpu_name memory_used/memory_total
"""
show_str_tot_lst = []

drv_ver = pml.nvmlSystemGetDriverVersion()
show_str_tot_lst.append('Driver Version: ' + str(drv_ver))
show_str_tot_lst.append('GPU card_name mem_used/mem_total   pid |        process_name       | user | mem_used')

for i in range(deviceCount):
    handle = pml.nvmlDeviceGetHandleByIndex(i)
    show_str_lst = []
    show_str_lst.append(str(i)+'  ')

    # 获取显卡全名
    card_name = pml.nvmlDeviceGetName(handle)
    card_name = ''.join(card_name.split(' ')[1:])
    show_str_lst.append(card_name)

    # 显存使用情况
    mem_info = pml.nvmlDeviceGetMemoryInfo(handle)
    mem_total = '{:>5}'.format(mem_info.total / mega) + 'M'
    mem_free =  '{:>5}'.format(mem_info.free / mega) + 'M'
    mem_used =  '{:>5}'.format(mem_info.used / mega) + 'M'
    show_str_lst.append('   ' + mem_used + '/' + mem_total)

    # 进程占用情况
    p_str = ''
    procs = pml.nvmlDeviceGetComputeRunningProcesses(handle)
    for j, p in enumerate(procs):
        #pid = '  ' + str(p.pid) + ' '
        pid = '{:<7}'.format(p.pid)
        p_name = ' {:<25} '.format(pml.nvmlSystemGetProcessName(p.pid))
        p_mem_used = ' ' + str(p.usedGpuMemory/mega) + 'M'

        pc = psutil.Process(procs[0].pid)
        p_user = ' {:<3} '.format(pc.username())

        p_str = ' ' + pid + '|' + p_name + '|' + p_user + '|' + p_mem_used

        if j==0:
            show_str_lst.append(p_str)
        else:
            show_str_lst.append('\n' + ' '*31 + p_str)

    t_t = ' '.join(show_str_lst)
    if i==0:
        show_str_tot_lst.append('='*90)
    else:
        show_str_tot_lst.append('-'*90)

    show_str_tot_lst.append(t_t)


pml.nvmlShutdown()

show_str = '\n'.join(show_str_tot_lst)
print(show_str)



#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function

__author__ = 'Zhuo Zhang'
__version__ = '0.1'
__description__ = 'nvue: An alternative to nvidia-smi'

import pynvml as pml
import psutil
from termcolor import colored

pml.nvmlInit()

# 显卡数量
deviceCount = pml.nvmlDeviceGetCount()

mega = 1024 * 1024

"""
gpu_id gpu_name memory_used/memory_total
"""
show_str_tot_lst = []

drv_ver = pml.nvmlSystemGetDriverVersion()
show_str_tot_lst.append('Driver Version: ' + bytes.decode(drv_ver))
show_str_tot_lst.append('{:<4}{:12}{:<13}{:6}{:6}{:8}{:12}{:8}{:<10}'.format('id','type', 'video memory', 'temp.', 'util.', 'pid', 'process', 'users', 'MemUsed'))

for i in range(deviceCount):
    handle = pml.nvmlDeviceGetHandleByIndex(i)
    show_str_lst = []
    show_str_lst.append(str(i)+'  ')

    # 获取显卡全名
    card_name = pml.nvmlDeviceGetName(handle)
    card_name = bytes.decode(card_name)
    card_name = ''.join(card_name.split(' ')[1:])
    show_str_lst.append(card_name)

    # 显存使用情况
    mem_info = pml.nvmlDeviceGetMemoryInfo(handle)
    mem_total = '{:6}'.format(mem_info.total // mega) + 'M'
    mem_free =  '{:6}'.format(mem_info.free // mega) + 'M'
    mem_used =  '{:<6}'.format(str(mem_info.used // mega) + 'M')
    show_str_lst.append('   ' + mem_used + '/' + mem_total)

    # 温度
    card_temp = ' ' + str(pml.nvmlDeviceGetTemperature(handle, pml.NVML_TEMPERATURE_GPU)) + 'C'
    show_str_lst.append(card_temp)

    # 利用率
    card_util_ratio = ' {:>3}'.format(pml.nvmlDeviceGetUtilizationRates(handle).gpu) + '%'
    show_str_lst.append(card_util_ratio)

    # 进程占用情况
    p_str = ''
    procs = pml.nvmlDeviceGetComputeRunningProcesses(handle)
    for j, p in enumerate(procs):
        #pid = '  ' + str(p.pid) + ' '
        pid = '{:<7}'.format(p.pid)
        p_name = bytes.decode(pml.nvmlSystemGetProcessName(p.pid))
        p_name = ' {:<10} '.format(p_name)
        p_mem_used = ' ' + str(p.usedGpuMemory//mega) + 'M'

        pc = psutil.Process(procs[0].pid)
        p_user = ' {:<8} '.format(pc.username())

        p_str = ' ' + pid + p_name + p_user + p_mem_used

        if j==0:
            show_str_lst.append(p_str)
        else:
            show_str_lst.append('\n' + ' '*31 + p_str)

    t_t = ' '.join(show_str_lst)
    if i==0:
        show_str_tot_lst.append('-'*90)

    show_str_tot_lst.append(t_t)


pml.nvmlShutdown()

show_str = '\n'.join(show_str_tot_lst)
print(show_str)



import pynvml
from loguru import logger
import traceback


def check_gpu(mem_required):
    try:
        pynvml.nvmlInit()
    except:
        logger.error('gpu init error:{}'.format(traceback.format_exc()))
        return []

    gpu_idx_list = []
    for gpu_idx in range(pynvml.nvmlDeviceGetCount()):
        handle = pynvml.nvmlDeviceGetHandleByIndex(gpu_idx)
        mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        mem_total, mem_free = mem_info.total / 1024 / 1024, mem_info.free / 1024 / 1024
        logger.info('mem_total:{}, mem_free:{}'.format(mem_total, mem_free))
        if mem_free > mem_required:
            logger.info('use gpu:{}'.format(gpu_idx))
            gpu_idx_list.append(gpu_idx)
    return gpu_idx_list

from traceback import extract_tb,format_list,format_exception_only
from os.path import isabs
import inspect

def get_func_args(func):
    return inspect.getargspec(func).args

def get_call_frame():
    for frame in inspect.stack():
        if not isabs(frame[1]):
            return frame
    return None

def get_trace_start(trace_obj):
    trace = extract_tb(trace_obj)
    for index,step in enumerate(trace):
        if not isabs(step[0]):
            return trace[index:]
    return []

def create_tb_str(err_type, val, tb_list):
    header = "Traceback (most recent call last):\n"
    tb_str = "".join(format_list(tb_list))
    exc_str = "".join(format_exception_only(err_type,val))
    return header + tb_str + exc_str

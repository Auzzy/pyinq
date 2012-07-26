from sys import exc_info
from traceback import extract_tb

from pyinq.util import create_tb_str

def test_raises(exception, func, *args, **kwargs):
    try:
        func(*args,**kwargs)
        return ""
    except exception:
        exc_type,exc_value,trace_obj = exc_info()[:3]
        trace = extract_tb(trace_obj)[1:]
        return create_tb_str(exc_type,exc_value,trace)

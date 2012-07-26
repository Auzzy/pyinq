"""
Copyright (c) 2012, Austin Noto-Moniz (metalnut4@netscape.net)

Permission to use, copy, modify, and/or distribute this software for any purpose
with or without fee is hereby granted, provided that the above copyright notice
and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
THIS SOFTWARE.
"""

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

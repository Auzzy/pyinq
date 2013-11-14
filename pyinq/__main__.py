"""
Copyright (c) 2012-2013, Austin Noto-Moniz (metalnut4@netscape.net)

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

"""
This is included to allow for test discovery from the command line
"""
from pyinq.parsers import install_command_parser,get_args,Parsers
from pyinq._pyinq import discover_tests_cmd,test_pyinq

install_command_parser(prog=__package__)
args,name = get_args()
if name==Parsers.DISCOVERY:
    discover_tests_cmd(**args)
elif name==Parsers.TEST:
    test_pyinq(**args)

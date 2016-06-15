#! /usr/bin/env python
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Takeshi HASEGAWA <hasegaw@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import json
import re
from subprocess import Popen, PIPE
import sys
import time

from area53 import route53


def run_expect(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, close_fds=True)
    (child_stdout, child_stdin) = (p.stdout, p.stdin)

    lines = child_stdout.read()

    if not isinstance(lines, str):
        lines = lines.decode('utf-8')

    lines = lines.split('\r')

    r = {'time': int(time.time())}

    for l in lines:
        m = re.search('^\s+PP IP Address Local: (\d+\.\d+\.\d+\.\d+),', l)
        if m:
            r['ip'] = m.group(1)
    return r


def get_current_ipaddr(host, passwd):
    cmd = './rtx1x00_show_status_pp_1.exp %s %s' % (host, passwd)
    r = run_expect(cmd)

    return r['ip']

# FIXME: Update with your own parameters.
ip = get_current_ipaddr('192.168.x.254', 'password')
zone = route53.get_zone('example.jp')
a_record = zone.get_a('hoge.example.jp')

old_ip = a_record.resource_records[0]
if old_ip == ip:
    sys.exit(0)

print('IP %s -> %s' % (old_ip, ip))
zone.update_a('hoge.example.jp', ip, 900)

try:
    import slackweb
except:
    sys.exit(0)

# FIXME: Update with your own parameters.
slack = slackweb.Slack(
    url='https://hooks.slack.com/services/xxxxx/yyyyy/zzzzz')
slack.notify(text='DNS record updated: %s' % ip, username='my_bot')

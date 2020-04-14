# ============  更改这里指定文件名 ===============
isp_ip_file = 'CHINANET-20200413.txt'  # 电信网络全部 IP 的文件名
bitnodes_files = [  # bitnodes.io 上面查出来的中国的 ip 的页面，保存成的 HTML 文件名
    'bitnodes1.htm',
    'bitnnodes2.htm',
    'bitnodes3.htm',
    'bitnodes4.htm',
    'bitnodes5.htm',
]
# ============  下面不要动  =====================

import re

IP_RE = re.compile('Node status">(.+?)</a')  # IP 正则匹配

def ip_to_int(ip):
    """
    :type ip: str
    :rtype: int
    """
    int_ = 0
    for i in ip.split('.'):
        int_ = int_ << 8 | int(i)

    return int_


def int_to_ip(int_):
    """
    :type int_: int
    :rtype: str
    """
    ip = []
    for _ in range(4):
        ip.append(str(int_ & 255))
        int_ >>= 8

    return '.'.join(ip[::-1])


with open(isp_ip_file) as f:
    isp_ip_list = [
        tuple(ip_to_int(ip) for ip in row.split('\t')[:2])
        for row in f.readlines()
    ]
isp_ip_list.sort()

res = []
for bitnodes_file in bitnodes_files:
    with open(bitnodes_file) as f:
        html = f.read()

    for i in IP_RE.finditer(html):
        ip = i.group(1)
        # 去掉ipv6
        if '[' in ip:
            continue
        ip_int = ip_to_int(ip.split(':')[0])
        for ip_left, ip_right in isp_ip_list:
            if ip_int < ip_left:
                continue
            elif ip_int <= ip_right:
                print(ip)
                res.append(f'{ip} {int_to_ip(ip_left)} {int_to_ip(ip_right)}')
                break

with open('../same_isp_bitnode.txt', 'w') as f:
    f.write('\n'.join(res))


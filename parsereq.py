import copy
import requests
import re
import urllib.parse


def parse(request, force_ssl=False):
    regex_header = re.compile(r'\s*([^:]+)\s*:\s*(.*)\s*')
    regex_cookie = re.compile(r'\s*([^;]+)\s*=\s*([^;]+)\s*')

    message = request.split('\n\n')
    msgmeta = message[0]
    http_data = message[1]

    msgmeta = msgmeta.split('\n')
    reqline = msgmeta[0].split(' ')
    http_method = reqline[0]
    http_path = reqline[1]

    http_headers = {}
    for header in msgmeta[1:]:
        match = regex_header.match(header)
        if match:
            http_headers[match.group(1)] = match.group(2)

    http_host = None
    http_cookies = None

    for k, v in copy.copy(http_headers).items():
        if 'host' == k.lower():
            http_host = v
            del http_headers[k]
        elif 'cookie' == k.lower():
            http_cookies = dict(regex_cookie.findall(v))
            del http_headers[k]
        if http_host and http_cookies:
            break

    if http_host.startswith('https://') or http_host.startswith('http://'):
        http_url = urllib.parse.urljoin(http_host, http_path)
    else:
        if force_ssl:
            http_url = urllib.parse.urljoin(
                'https://{}'.format(http_host), http_path)
        else:
            http_url = urllib.parse.urljoin(
                'http://{}'.format(http_host), http_path)
        
    return requests.Request(http_method, http_url, cookies=http_cookies,
                            headers=http_headers, data=http_data)


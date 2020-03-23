import parsereq
import requests


def main():
    r = '''GET /robots.txt HTTP/1.1
    User-Agent: Mozilla/4.0 (compatible; MSIE5.01; Windows NT)
    Host: github.com
    Content-Type: text/html
    Accept-Language: en-us
    Accept-Encoding: gzip, deflate
    Connection: Keep-Alive

    '''

    r = parsereq.parse(r, force_ssl=True).prepare()
    s = requests.Session()
    print(s.send(r).content)


if __name__ == '__main__':
    main()


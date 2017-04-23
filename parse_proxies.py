import re

def parseProxies():
    with open('proxies.txt') as f:
        for line in f:
            line = re.sub(r'^.+China.+$', '', line)

    with open('proxies.txt') as f:
        for line in f:
            line = re.sub(r'^(.+)#.+$',r'\1', line)

    with open('proxies.txt', 'r') as f:
        proxyList = [line[:-1] for line in f]
        return proxyList


if __name__ == '__main__':
    parseProxies()

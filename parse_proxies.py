import re

def parseProxies():
    with open('fetched_proxies.txt') as old_file:
        with open('proxies.txt', 'w') as new_file:
            for line in old_file:
                line = re.sub(r'^.+China.+$', '', line)
                line = re.sub(r'^(.+)#.+$',r'\1', line)
                if line != '':
                    new_file.write(line)

    with open('proxies.txt', 'r') as f:
        proxyList = [line[:-1] for line in f]
        return proxyList


if __name__ == '__main__':
    parseProxies()

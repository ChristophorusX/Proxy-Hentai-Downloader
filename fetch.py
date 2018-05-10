#!/usr/bin/env python

import sys
import json
import optparse
import os
import queue as py3queue
import random
import re
import string
import subprocess
import threading
import time
import base64
import urllib.request, urllib.error, urllib.parse


VERSION = "2.017"
BANNER = ">>>>>>>>>> Fetching Proxies (version %s) <<<<<<<<<<" % VERSION

ANONIMITY_LEVELS = {"high": "elite", "medium": "anonymous", "low": "transparent"}
FALLBACK_METHOD = False
IFCONFIG_CANDIDATES = ("https://ifconfig.co/ip", "https://api.ipify.org/?format=text", "https://ifconfig.io/ip", "https://ifconfig.minidump.info/ip", "https://myexternalip.com/raw", "https://wtfismyip.com/text")
IFCONFIG_URL = None
MAX_HELP_OPTION_LENGTH = 18
PROXY_LIST_URL = "https://raw.githubusercontent.com/stamparm/aux/master/fetch-some-list.txt"
ROTATION_CHARS = ('/', '-', '\\', '|')
TIMEOUT = 10
THREADS = 10
USER_AGENT = "curl/7.{curl_minor}.{curl_revision} (x86_64-pc-linux-gnu) libcurl/7.{curl_minor}.{curl_revision} OpenSSL/0.9.8{openssl_revision} zlib/1.2.{zlib_revision}".format(curl_minor=random.randint(8, 22), curl_revision=random.randint(1, 9), openssl_revision=random.choice(string.ascii_lowercase), zlib_revision=random.randint(2, 6))

options = None
counter = [0]
threads = []

def retrieve(url, data=None, headers={"User-agent": USER_AGENT}, timeout=TIMEOUT, opener=None):
    try:
        req = urllib.request.Request("".join(url[i].replace(' ', "%20") if i > url.find('?') else url[i] for i in range(len(url))), data, headers)
        retval = (urllib.request.urlopen if not opener else opener.open)(req, timeout=timeout).read()
    except Exception as ex:
        try:
            retval = ex.read() if hasattr(ex, "read") else getattr(ex, "msg", str())
        except:
            retval = None

    return retval or ""

def worker(queue, handle=None):
    try:
        while True:
            proxy = queue.get_nowait()
            result = ""
            counter[0] += 1
            sys.stdout.write("\r%s\r" % ROTATION_CHARS[counter[0] % len(ROTATION_CHARS)])
            sys.stdout.flush()
            start = time.time()
            candidate = "%s://%s:%s" % (proxy["proto"], proxy["ip"], proxy["port"])
            if not all((proxy["ip"], proxy["port"])) or re.search(r"[^:/\w.]", candidate):
                continue
            if not FALLBACK_METHOD:
                process = subprocess.Popen("curl -m %d -A \"%s\" --proxy %s %s" % (TIMEOUT, USER_AGENT, candidate, IFCONFIG_URL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                result, _ = process.communicate()
            elif proxy["proto"] in ("http", "https"):
                opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": candidate, "https": candidate}))
                result = retrieve(IFCONFIG_URL, timeout=options.maxLatency or TIMEOUT, opener=opener)
            if (result or "").strip() == proxy["ip"].encode("utf8"):
                latency = time.time() - start
                if latency < (options.maxLatency or TIMEOUT):
                    sys.stdout.write("\r%s%s # latency: %.2f sec; country: %s; anonymity: %s (%s)\n" % (candidate, " " * (32 - len(candidate)), latency, ' '.join(_.capitalize() for _ in (proxy["country"].lower() or '-').split(' ')), proxy["type"], proxy["anonymity"]))
                    sys.stdout.flush()
                    if handle:
                        candidate = candidate + os.linesep
                        candidate = candidate.encode("utf-8")
                        # candidate = base64.b64encode(candidate)
                        os.write(handle, candidate)
    except py3queue.Empty:
        pass

def run():
    global FALLBACK_METHOD
    global IFCONFIG_URL

    options.outputFile = 'fetched_proxies.txt'

    sys.stdout.write(">>>>>>>>>> FETCH SOME PROXIES <<<<<<<<<<\n")
    sys.stdout.write("[i] initial testing...\n")

    for candidate in IFCONFIG_CANDIDATES:
        result = retrieve(candidate).decode('utf-8')
        if re.search(r"\A\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\Z", (result or "").strip()):
            IFCONFIG_URL = candidate
            break

    process = subprocess.Popen("curl -m %d -A \"%s\" %s" % (TIMEOUT, USER_AGENT, IFCONFIG_URL), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, _ = process.communicate()
    stdout = stdout.decode('utf-8')
    FALLBACK_METHOD = re.search(r"\d+\.\d+\.\d+\.\d+", stdout or "") is None

    sys.stdout.write("[i] retrieving list of proxies...\n")
    try:
        proxies = json.loads(retrieve(PROXY_LIST_URL, headers={"User-agent": USER_AGENT}))
    except:
        exit("[!] something went wrong during the proxy list retrieval/parsing. Please check your network settings and try again")
    random.shuffle(proxies)

    if options.country or options.anonymity or options.type:
        _ = []
        for proxy in proxies:
            if options.country and not re.search(options.country, proxy["country"], re.I):
                continue
            if options.anonymity and not re.search(options.anonymity, "%s (%s)" % (proxy["anonymity"], ANONIMITY_LEVELS.get(proxy["anonymity"].lower(), "")), re.I):
                continue
            if options.type and not re.search(options.type, proxy["proto"], re.I):
                continue
            _.append(proxy)
        proxies = _


    if options.outputFile:
        handle = os.open(options.outputFile, os.O_APPEND | os.O_CREAT | os.O_TRUNC | os.O_WRONLY)
        sys.stdout.write("[i] storing results to '%s'...\n" % options.outputFile)
    else:
        handle = None

    queue = py3queue.Queue()
    for proxy in proxies:
        queue.put(proxy)

    sys.stdout.write("[i] testing %d proxies (%d threads)...\n\n" % (len(proxies), options.threads or THREADS))
    for _ in range(options.threads or THREADS):
        thread = threading.Thread(target=worker, args=[queue, handle])
        thread.daemon = True

        try:
            thread.start()
        except:
            sys.stderr.write("[x] error occurred while starting new thread")
            break

        threads.append(thread)

    try:
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)
    except KeyboardInterrupt:
        sys.stderr.write("\r   \n[!] Ctrl-C pressed\n")
    else:
        sys.stdout.write("\n[i] done\n")
    finally:
        sys.stdout.flush()
        sys.stderr.flush()
        if handle:
            os.close(handle)
        os._exit(0)

def main():
    global options

    sys.stdout.write("%s\n\n" % BANNER)
    parser = optparse.OptionParser(version=VERSION)
    parser.add_option("--anonymity", dest="anonymity", help="Regex for filtering anonymity (e.g. \"anonymous|elite\")")
    parser.add_option("--country", dest="country", help="Regex for filtering country (e.g. \"china|brazil\")")
    parser.add_option("--max-latency", dest="maxLatency", type=float, help="Maximum (tolerable) latency in seconds (default %d)" % TIMEOUT)
    parser.add_option("--output", dest="outputFile", help="Store resulting proxies to output file")
    parser.add_option("--threads", dest="threads", type=int, help="Number of scanning threads (default %d)" % THREADS)
    parser.add_option("--type", dest="type", help="Regex for filtering proxy type (e.g. \"http\")")

    # Dirty hack(s) for help message
    def _(self, *args):
        retVal = parser.formatter._format_option_strings(*args)
        if len(retVal) > MAX_HELP_OPTION_LENGTH:
            retVal = ("%%.%ds.." % (MAX_HELP_OPTION_LENGTH - parser.formatter.indent_increment)) % retVal
        return retVal

    parser.formatter._format_option_strings = parser.formatter.format_option_strings
    parser.formatter.format_option_strings = type(parser.formatter.format_option_strings)(_, parser)

    for _ in ("-h", "--version"):
        option = parser.get_option(_)
        option.help = option.help.capitalize()

    try:
        options, _ = parser.parse_args()
    except SystemExit:
        print()
        raise

    run()

if __name__ == "__main__":
    main()

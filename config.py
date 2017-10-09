import parse_proxies

dir = "/Volumes/Seagate/Manga"
download_ori = False
download_thread_cnt = 5
scan_thread_cnt = 1
proxy = parse_proxies.parseProxies()
log_path = "eh.log"
log_verbose = 2
rename_ori = False
daemon = False
rpc_interface = 'localhost'
rpc_port = None
rpc_secret = None
save_tasks = False
make_archive = False

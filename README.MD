# Proxy Hentai Downloader

## General

This is a python project supporting download from e-hentai and ex-hentai galleries (with the help of proxies) while automatically searching for available proxies. We combine two existing projects from GitHub: [fffonion/xeHentai](https://github.com/fffonion/xeHentai) and [stamparm/fetch-some-proxies](https://github.com/stamparm/fetch-some-proxies) to release users from the burden of having to search for working proxies every time using the downloader.

## Requirements

- Python 3.x

## Installation

### Install Proxy Hentai Downloader

```bash
$ git clone https://github.com/ChristophorusX/Proxy-Hentai-Downloader.git
```

## Get Started

Run `./AutoDownload` to start download.

```bash
$ ./AutoDownload
```

To download from exhentai galleries, put your username and password as flags, e.g.

```bash
$ ./AutoDownload -u <your username> -k <your password>
```

To skip the step of proxy searching, put `-s/--skip` flag.

### Set URLs

All URLs waiting for download can be put into the file `urls.txt`. NOTE: URLs should be separated by spaces in order to be read by the program.

### Set Configurations

There are two `config.py` located at project home directory and `./xeHentai`. The first one is the custom configuration file for users, and the second is a fallback option, of which the modification is not recommended in general.

- **dir** Directory for downloaded files, default as current directory
- **download_ori** Whether download original image, default as False
- **download_thread_cnt** Number of download thread, default as 5
- **scan_thread_cnt** Number of scan thread, default as 1
- **proxy** List of proxies, such as `["socks://127.0.0.1:1080", "http://127.0.0.1:8080"]`
- **proxy_image** Whether use proxies for download (otherwise proxies are only used for scanning), default as True
- **log_path** Log path, default as `eh.log`
- **log_verbose** Verbose level of log, from 1-3, default as 2
- **rename_ori** Name images with original names (otherwise with number), default as False
- **daemon** Background mode, default as False
- **rpc_interface** RPC interface IP, default as `localhost`
- **rpc_port** RPC port, default as `None`
- **rpc_secret** RPC secret, default as `None`
- **save_tasks** Whether save missions to `h.json`, default as False
- **make_archive** Whether produce zip pack and delete original file after downloading, default as False

### Logging In

In order to download image from ex-hentai gallery, one needs to provide user name and password to the program. This can be achieved by providing flags `-u/--username` and `-k/--key` to `AutoDownload` as mentioned above.

### Filtering Proxies

One can choose whether or not to run the proxy searching program before each download. The skipping of the proxy search can be done by providing `-s/--skip` flag.

### Getting gallery items from favorites

The helping script `extractor.py` can extract target address from the source (html) page of your gallery.

## Legal Issues

This software is distributed under the MIT license.

In particular, please be aware that

> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

We only ship the code here, and how you are going to use it is left to your own discretion.

## Author

Made by [@ChristophorusX](https://github.com/ChristophorusX)

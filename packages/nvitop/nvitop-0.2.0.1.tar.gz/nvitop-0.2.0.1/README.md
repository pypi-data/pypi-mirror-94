# nvitop

![Python 3.5+](https://img.shields.io/badge/Python-3.5%2B-brightgreen.svg)
![PyPI](https://img.shields.io/pypi/v/nvitop?label=PyPI)
![status](https://img.shields.io/pypi/status/nvitop)
![Top Language](https://img.shields.io/github/languages/top/XuehaiPan/nvitop?label=Python)
![License](https://img.shields.io/github/license/XuehaiPan/nvitop?label=License)

An interactive Nvidia-GPU process viewer.

This project is inspired by [nvidia-htop](https://github.com/peci1/nvidia-htop), a tool for enriching the output of `nvidia-smi`. [nvidia-htop](https://github.com/peci1/nvidia-htop) uses regular expressions to read the output of `nvidia-smi` from a subprocess, which is inefficient. Meanwhile, there is a powerful interactive GPU monitoring tool called [nvtop](https://github.com/Syllo/nvtop). But [nvtop](https://github.com/Syllo/nvtop) is written in *C*, which makes it lack of portability. And it is really inconvenient that you should compile it yourself during installation. Therefore, I made this repo. I got a lot help when reading the source code of [ranger](https://github.com/ranger/ranger), the console file manager. Some files in this repo are copied and modified from [ranger](https://github.com/ranger/ranger) under the GPLv3 License.

## Features

- **Informative and fancy output**: show more information than `nvidia-smi` with colorized fancy box drawing.
- **Monitor mode**: can run as a resource monitor, rather than print the results only once. (vs. [nvidia-htop](https://github.com/peci1/nvidia-htop), limited support with command `watch -c`)
- **Interactive**: responsive for user inputs in monitor mode. (vs. [py3nvml](https://github.com/fbcotter/py3nvml))
- **Efficiency**:
  - query device status using [*NVML Python bindings*](https://pypi.org/project/nvidia-ml-py) directly and cache them with `ttl_cache` from [cachetools](https://github.com/tkem/cachetools), instead of parsing the output of `nvidia-smi`. (vs. [nvidia-htop](https://github.com/peci1/nvidia-htop))
  - display information using the `curses` library rather than `print` with ANSI escape codes. (vs. [py3nvml](https://github.com/fbcotter/py3nvml))
- **Portability**: work on both Linux and Windows.
  - get host process information using the cross-platform library [psutil](https://github.com/giampaolo/psutil) instead of calling `ps -p <pid>` in a subprocess. (vs. [nvidia-htop](https://github.com/peci1/nvidia-htop) & [py3nvml](https://github.com/fbcotter/py3nvml))
  - written in pure Python, easy to install with `pip`. (vs. [nvtop](https://github.com/Syllo/nvtop))

## Requirements

- Python 3.5+
- curses
- nvidia-ml-py
- psutil
- cachetools
- termcolor

## Installation

Install from PyPI:

```bash
$ pip install nvitop
```

Install the latest version from GitHub:

```bash
$ pip install git+https://github.com/XuehaiPan/nvitop.git#egg=nvitop
```

Or, clone this repo and install manually:

```bash
$ git clone --depth=1 https://github.com/XuehaiPan/nvitop.git
$ cd nvitop
$ pip install .
```

## Usage

Query the device and process status. The output is similar to `nvidia-smi`, but has been enriched and colorized.

```bash
# Query status of all devices
$ nvitop

# Specify query devices
$ nvitop -o 0 1  # only show <GPU 0> and <GPU 1>
```

Run as a resource monitor, like `htop`:

```bash
# Automatically configure the display mode according to the terminal size
$ nvitop -m

# Forcibly display as `full` mode
$ nvitop -m full

# Forcibly display as `compact` mode
$ nvitop -m compact

# Specify query devices
$ nvitop -m -o 0 1  # only show <GPU 0> and <GPU 1>

# Only show devices in `CUDA_VISIBLE_DEVICES`
$ nvitop -m -ov
```

Press `q` to return to the terminal.

Type `nvitop --help` for more information:

```
usage: nvitop [-h] [-m [{auto,full,compact}]] [-o idx [idx ...]] [-ov]
              [--gpu-util-thresh th1 th2] [--mem-util-thresh th1 th2]

A interactive Nvidia-GPU process viewer.

optional arguments:
  -h, --help            show this help message and exit
  -m [{auto,full,compact}], --monitor [{auto,full,compact}]
                        Run as a resource monitor. Continuously report query data,
                        rather than the default of just once.
                        If no argument is specified, the default mode `auto` is used.
  -o idx [idx ...], --only idx [idx ...]
                        Only show devices specified, suppress option `-ov`.
  -ov, --only-visible   Only show devices in environment variable `CUDA_VISIBLE_DEVICES`.
  --gpu-util-thresh th1 th2
                        Thresholds of GPU utilization to distinguish load intensity.
                        Coloring rules: light < th1 % <= moderate < th2 % <= heavy.
                        ( 1 <= th1 < th2 <= 99, defaults: 10 75 )
  --mem-util-thresh th1 th2
                        Thresholds of GPU memory utilization to distinguish load intensity.
                        Coloring rules: light < th1 % <= moderate < th2 % <= heavy.
                        ( 1 <= th1 < th2 <= 99, defaults: 10 80 )
```

## Screenshots

![Screen Recording](https://user-images.githubusercontent.com/16078332/107397216-6ebb2b00-6b39-11eb-9263-35e660bb82df.gif)

Example output of `nvitop`:

<img src="https://user-images.githubusercontent.com/16078332/107397202-6a8f0d80-6b39-11eb-8bea-62ff63a44088.png" alt="Screenshot">

Example output of `nvitop -m`:

<table>
  <tr valign="center">
    <td align="center">Full</td>
    <td align="center">Compact</td>
  </tr>
  <tr valign="top">
    <td align="center"><img src="https://user-images.githubusercontent.com/16078332/107397207-6bc03a80-6b39-11eb-8ce2-0c84d358de52.png" alt="Full"></td>
    <td align="center"><img src="https://user-images.githubusercontent.com/16078332/107397209-6cf16780-6b39-11eb-8766-8767b551f13f.png" alt="Compact"></td>
  </tr>
</table>

## License

GNU General Public License, version 3 (GPLv3)

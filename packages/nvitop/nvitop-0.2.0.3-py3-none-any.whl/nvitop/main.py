# This file is part of nvitop, the interactive Nvidia-GPU process viewer.
# License: GNU GPL version 3.

import argparse
import os
import sys

import pynvml as nvml

from .device import Device
from .libcurses import libcurses
from .top import Top
from .utils import colored


def parse_arguments():
    coloring_rules = '{} < th1 %% <= {} < th2 %% <= {}'.format(colored('light', 'green'),
                                                               colored('moderate', 'yellow'),
                                                               colored('heavy', 'red'))
    parser = argparse.ArgumentParser(prog='nvitop', description='A interactive Nvidia-GPU process viewer.',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-m', '--monitor', type=str, default='notpresented',
                        nargs='?', choices=['auto', 'full', 'compact'],
                        help='Run as a resource monitor. Continuously report query data,\n' +
                             'rather than the default of just once.\n' +
                             'If no argument is given, the default mode `auto` is used.')
    parser.add_argument('-o', '--only', type=int, nargs='+', metavar='idx',
                        help='Only show the specified devices, suppress option `-ov`.')
    parser.add_argument('-ov', '--only-visible', action='store_true',
                        help='Only show devices in environment variable `CUDA_VISIBLE_DEVICES`.')
    parser.add_argument('--gpu-util-thresh', type=int, nargs=2, choices=range(1, 100), metavar=('th1', 'th2'),
                        help='Thresholds of GPU utilization to distinguish load intensity.\n' +
                             'Coloring rules: {}.\n'.format(coloring_rules) +
                             '( 1 <= th1 < th2 <= 99, defaults: {} {} )'.format(*Device.GPU_UTILIZATION_THRESHOLDS))
    parser.add_argument('--mem-util-thresh', type=int, nargs=2,
                        choices=range(1, 100), metavar=('th1', 'th2'),
                        help='Thresholds of GPU memory utilization to distinguish load intensity.\n' +
                             'Coloring rules: {}.\n'.format(coloring_rules) +
                             '( 1 <= th1 < th2 <= 99, defaults: {} {} )'.format(*Device.MEMORY_UTILIZATION_THRESHOLDS))
    args = parser.parse_args()
    if args.monitor is None:
        args.monitor = 'auto'
    if args.monitor != 'notpresented' and not (sys.stdin.isatty() and sys.stdout.isatty()):
        print('Error: Must run nvitop monitor mode from terminal', file=sys.stderr)
        return 1
    if args.gpu_util_thresh is not None:
        Device.GPU_UTILIZATION_THRESHOLDS = tuple(sorted(args.gpu_util_thresh))
    if args.mem_util_thresh is not None:
        Device.MEMORY_UTILIZATION_THRESHOLDS = tuple(sorted(args.mem_util_thresh))

    return args


def main():
    args = parse_arguments()

    try:
        nvml.nvmlInit()
    except nvml.NVMLError_LibraryNotFound as error:  # pylint: disable=no-member
        print('Error: {}'.format(error), file=sys.stderr)
        return 1

    device_count = nvml.nvmlDeviceGetCount()
    if args.only is not None:
        visible_devices = set(args.only)
    elif args.only_visible:
        try:
            visible_devices = set(map(int, filter(lambda s: s != '' and not s.isspace(),
                                                  os.getenv('CUDA_VISIBLE_DEVICES').split(','))))
        except (ValueError, AttributeError):
            visible_devices = set(range(device_count))
    else:
        visible_devices = set(range(device_count))
    devices = list(map(Device, sorted(set(range(device_count)).intersection(visible_devices))))

    if args.monitor != 'notpresented' and len(devices) > 0:
        with libcurses() as win:
            top = Top(devices, mode=args.monitor, win=win)
            top.loop()
    else:
        top = Top(devices)
    top.print()
    top.destroy()

    nvml.nvmlShutdown()

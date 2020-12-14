#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

# API documentation — https://github.com/rm-hull/luma.led_matrix

####### MOVE TO READ ME #######
# run in rpi
# https://luma-led-matrix.readthedocs.io/en/latest/install.html#pre-requisites

import re
import time
import argparse

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

parser = argparse.ArgumentParser(description='matrix_demo arguments',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
parser.add_argument('--block-orientation', type=int, default=0, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
parser.add_argument('--reverse-order', type=bool, default=False, help='Set to true if blocks are in reverse order')

args = parser.parse_args()

class matrix:
    def __init__(self, n, block_orientation, rotate, inreverse):
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, cascaded=n or 1, block_orientation=block_orientation,
                         rotate=rotate or 0, blocks_arranged_in_reverse_order=inreverse)
        print("Created device")

    def notif(self):
        self.device.clear()
        # pair this with notification visual with a sound being played ?
        msg = "Notification"
        print(msg)

        time.sleep(1)
        with canvas(self.device) as draw:
            text(draw, (1, 0), chr(33), fill="white")

        time.sleep(0.3)
        for _ in range(5):
            self.device.contrast(0x00)
            time.sleep(0.3)
            self.device.contrast(0x80)
            time.sleep(0.3)

        self.device.contrast(0x80)
        time.sleep(0.3)

    def breathe(self):
        self.device.clear()
        msg = "Breathe"
        print(msg)

        time.sleep(1)
        with canvas(self.device) as draw:
            text(draw, (0, 0), chr(7), fill="white")

        time.sleep(1)
        num_reps = 3
        for _ in range(num_reps):
            for intensity in range(2, 16):
                self.device.contrast(intensity * 16)
                time.sleep(0.3)
            for intensity in reversed(range(16)):
                self.device.contrast(intensity * 16)
                time.sleep(0.3)

        self.device.contrast(0x80)
        time.sleep(0.3)

    def congrats(self):
        self.device.clear()
        # pair this with notification visual with a sound being played ?
        msg = "Congrats"
        print(msg)

        time.sleep(1)
        with canvas(self.device) as draw:
            text(draw, (0, 0), chr(1), fill="white")

        time.sleep(0.3)
        for _ in range(5):
            self.device.contrast(0x00)
            time.sleep(0.3)
            self.device.contrast(0x80)
            time.sleep(0.3)

        self.device.contrast(0x80)
        time.sleep(0.3)


    def erase(self):
        self.device.cleanup()


def run_breathe():
    try:
        device = matrix(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
        device.breathe()
        device.erase()
    except KeyboardInterrupt:
        pass

def run_reminder():
    try:
        device = matrix(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
        device.notif()
        device.erase()
    except KeyboardInterrupt:
        pass

def run_congrats():
    try:
        device = matrix(args.cascaded, args.block_orientation, args.rotate, args.reverse_order)
        device.congrats()
        device.erase()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    run_congrats()

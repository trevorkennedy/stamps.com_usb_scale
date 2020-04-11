#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
"""
Handling raw data inputs example
"""
from time import sleep
from msvcrt import kbhit

import pywinusb.hid as hid

def sample_handler(data):
    dat = data[4:]
    rawounces = (dat[0]+(dat[1]*255))*1.0/10
    pounds = int(rawounces)/16
    ounces = rawounces%16
    print pounds,"lbs ",ounces,"oz"
    #print("Raw data: {0}".format(data))

def raw_test(scale_name):
    # simple test
    # browse devices...
    all_hids = hid.find_all_hid_devices()
    if all_hids:
        while True:
            correctindex = -1
            for index, device in enumerate(all_hids):
                print(device.vendor_name)
                if device.vendor_name == scale_name:
                    correctindex = index
            index_option = correctindex+1
            break;
        int_option = int(index_option)
        if int_option:
            device = all_hids[int_option-1]
            try:
                device.open()

                #set custom raw data handler
                device.set_raw_data_handler(sample_handler)

                print("\nWaiting for data...\nPress any (system keyboard) key to stop...")
                try:
                    while not kbhit() and device.is_plugged():
                        #just keep the device opened to receive events
                        sleep(0.5)
                except:
                    sys.exit()
                return
            finally:
                device.close()
    else:
        print("There's not any non system HID class device available")
#
if __name__ == '__main__':
    # first be kind with local encodings
    import sys
    if sys.version_info >= (3,):
        # as is, don't handle unicodes
        unicode = str
        raw_input = input
    else:
        # allow to show encoded strings
        import codecs
        sys.stdout = codecs.getwriter('mbcs')(sys.stdout)
    raw_test("X.J.GROUP")

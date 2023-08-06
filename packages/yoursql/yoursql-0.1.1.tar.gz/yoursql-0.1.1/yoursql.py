#!/usr/bin/env python

import os

def main():
    for root, dirs, files in os.walk("."):
        path = root.split(os.sep)
        print((len(path) - 1) * '------', os.path.basename(root))
        for file in files:
            if file.endswith('.sql'):
                print(len(path) * '---', file)
#!/usr/bin/env python3

import os
import sys

def main():
    command = sys.argv[0]
    command_dir = os.path.dirname(command)[:-3]
    sys.path.append(command_dir)

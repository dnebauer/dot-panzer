#!/usr/bin/env python3
# encoding: utf-8

import sys

INPUT_LINES = sys.stdin.readlines()
OUTPUT_LINES = []
CLOSED = False

for line in INPUT_LINES:
    if not CLOSED and line == '...\n':
        OUTPUT_LINES.append('---\n')
        CLOSED = True
    else:
        OUTPUT_LINES.append(line)

for line in OUTPUT_LINES:
    sys.stdout.write(line)

sys.stdout.flush()

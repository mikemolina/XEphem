#! /bin/sh
grep 'PATCHLEVEL' GUI/xephem/patchlevel.c | sed 's/.*\([0-9]\.[0-9]\.[0.9]\).*/\1/'

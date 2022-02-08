#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from _datacore import df

for i,f in enumerate(df.columns):
  print(i, "\t", f)


#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pandas as pd
from numpy import NaN
from sys import argv

if len(argv) != 2:
  print("Δώστε όνομα αρχείου για να συνεχίσετε")
  exit(1)

INFILE = argv[1]

try:
  df = pd.read_csv(INFILE)
except:
  print("Αδύνατη η ανάγνωση του αρχείου {}".format(INFILE))
  exit(2)

def check_data(raw = False):
  if raw:
    if df.columns[0] == "Α/Α":
      print("Το αρχείο δεδομένων έχει περάσει ήδη προετοιμασία!")
      exit(3)

    elif df.columns[0] != "Χρονική σήμανση":
      print("Το αρχείο δεδομένων δεν φαίνεται να είναι έγκυρο!")
      exit(3)

  else:
    if df.columns[0] == "Χρονική σήμανση":
      print("Το αρχείο δεδομένων δεν έχει περάσει προετοιμασία!")
      exit(3)

    elif df.columns[0] != "Α/Α":
      print("Το αρχείο δεδομένων δεν φαίνεται να είναι έγκυρο!")
      exit(3)

  

#!/usr/bin/env python3
#-*- coding: utf-8 -*-

def underlined(s, c='='):
  return s+"\n"+(c*len(s))

def clear_screen():
  print("\033[2J", end="")

def save_screen():
  print("\033[?47h", end="")

def restore_screen():
  print("\033[?47l", end="")

def pause():
  print("\nΠιέστε οποιοδήποτε πλήκτρο για συνέχεια ή ^C για έξοδο.")
  try:
    input()
  except KeyboardInterrupt:
    print("\rΑκυρώθηκε από τον/-ην χρήστη/-τρια.")
    exit(0)
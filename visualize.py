#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from _datacore import df, NaN, check_data, pd
from _format   import *

import curses
from curses.textpad import Textbox

check_data()


### Προκαθορισμένες παλέττες
IMPORTANCE_PALETTE = ['#C44040','#C46C40','#C49840','#C4C440','#98C440','#6CC440','#40C440']
AGREEMENT_PALETTE  = ['#C44040','#C49840','#D5B900','#98C440','#40C440']
YES_NO_PALETTE     = ['#C44040','#40C440','#CCCCCC']

### Συναρτήσεις σωστής ταξινόμισης
def sort_age(key):
  if key == "Κάτω των 18":
    return "18+"
  elif key == "Άνω των 57":
    return "57-"
  else:
    return key

def sort_education(key):
  PREDEFINED = ['Δημοτικό','Γυμνάσιο','Λύκειο','ΙΕΚ','Πανεπιστήμιο ΑΕΙ/ΑΤΕΙ','Μεταπτυχιακό/Διδακτορικό']

  if key in PREDEFINED:
    return "{} {}".format(PREDEFINED.index(key),key)

  return "99 {}".format(key)

def sort_importance(key):
  VALUES = {'Καθόλου':1, 'Λίγο':2, 'Αρκετά':3, 'Πολύ':4, 'Πάρα πολύ':5, 'Απόλυτα':6}

  if key in VALUES:
    return VALUES[key]

  return 99

def sort_agreement(key):
  VALUES = {'Διαφωνώ απόλυτα':1, 'Διαφωνώ':2, 'Ούτε συμφωνώ ούτε διαφωνώ':3, 'Συμφωνώ':4, 'Συμφωνώ απόλυτα':5}

  if key in VALUES:
    return VALUES[key]

  return 99

def sort_pcheck_frequence(key):
  VALUES = {'Ποτέ':1, 'Μόνο όταν υποψιάζομαι κάτι':2, 'Σπάνια':3, 'Συχνά':4}

  if key in VALUES:
    return VALUES[key]

  return 99

def sort_boolean(key):
  # Αυτή η "βαθμολόγηση" συμβάλλει μόνον στην σωστή απόδοση χρωμάτων
  VALUES = {'Όχι':1,'Αρνητικά':1,'Ναι':2,'Θετικά':2}

  if key in VALUES:
    return VALUES[key]

  return 3

def sort_privacy_policy(key):
  # Αυτή η "βαθμολόγηση" συμβάλλει μόνον στην σωστή απόδοση χρωμάτων
  VALUES = {'Ναι, και την κατάλαβα':1,'Ναι, αλλά δεν την κατάλαβα':2,'Όχι':3,'Δεν ξέρω τι είναι η πολιτική απορρήτου':4}

  return VALUES[key]

def sort_cookies(key):
  VALUES=["Όλα","Μόνο τα απαραίτητα","Απλώς κλείνω το σχετικό παραθυράκι που αναδύεται και το προσπερνώ","Δεν ξέρω/δε θυμάμαι"]

  return VALUES.index(key)+1

### Συναρτήσεις οπτικοποίησης
def vis_gender():
  return vis_pie(1,  "Φύλο", colours=['royalblue','magenta','lightgray'])

def vis_age():
  return vis_pie(2,  "Ηλικία", colours=['#FFCDDA','#FFA5BD','#FF7DA0','#FF5582','#FF2D65'], custom_sort=sort_age)

def vis_education():
  return vis_pie(3,  "Επίπεδο εκπαίδευσης", custom_sort=sort_education)

def vis_fb_importance():
  return vis_pie(5,  "Σημαντικότητα", colours=IMPORTANCE_PALETTE, custom_sort=sort_importance)

def vis_accept_friend_requests():
  return vis_pie(14, "Άποψη", colours=YES_NO_PALETTE, custom_sort=sort_boolean)

def vis_privacy_check():
  return vis_pie(17, "Συχνότητα", colours=IMPORTANCE_PALETTE, custom_sort=sort_pcheck_frequence)

def vis_privacy_worry():
  return vis_pie(18, "Άποψη", colours=IMPORTANCE_PALETTE, custom_sort=sort_importance)

def vis_privacy_policy():
  return vis_pie(19, "Άποψη", colours=['#40C440','#C4C440','#C44040','#CCCCCC'], custom_sort=sort_privacy_policy)

def vis_cookies():
  return vis_pie(21, "Άποψη", custom_sort=sort_cookies)

def vis_decentralized():
  return vis_pie(22, "Άποψη", colours=YES_NO_PALETTE, custom_sort=sort_boolean)

def vis_delete_fb():
  return vis_pie(28, "Άποψη", colours=AGREEMENT_PALETTE, custom_sort=sort_agreement)

def vis_fb_tip():
  return vis_pie(29, "Άποψη")

def vis_why_fb():
  return vis_pie(4,  "Άτομα", True)

def vis_real_data():
  return vis_bar(6,  "Άτομα", multiple=True, colours='#C45D5F')

def vis_positive_friend_because():
  return vis_bar(15, "Άτομα", multiple=True, colours='#C45D5F')

def vis_true_or_false():
  return vis_bar(16, "Άτομα", multiple=True, colours='#C45D5F')

def vis_data_uses():
  return vis_bar(20, "Άτομα", multiple=True, colours='#C45D5F')

VISUALIZEABLE = {
  df.columns[1]:  vis_gender,
  df.columns[2]:  vis_age,
  df.columns[3]:  vis_education,
  df.columns[4]:  vis_why_fb,
  df.columns[5]:  vis_fb_importance,
  df.columns[6]:  vis_real_data,
  df.columns[14]: vis_accept_friend_requests,
  df.columns[15]: vis_positive_friend_because,
  df.columns[16]: vis_true_or_false,
  df.columns[17]: vis_privacy_check,
  df.columns[18]: vis_privacy_worry,
  df.columns[19]: vis_privacy_policy,
  df.columns[20]: vis_data_uses,
  df.columns[21]: vis_cookies,
  df.columns[22]: vis_decentralized,
  df.columns[28]: vis_delete_fb,
  df.columns[29]: vis_fb_tip
}


### Βοηθητικές συναρτήσεις
def vis_name_by_id(i):
  return list(VISUALIZEABLE.keys())[i]

def vis_func_by_id(i):
  return VISUALIZEABLE[vis_name_by_id(i)]

def get_data_basic(column_id, label, custom_sort):
  data = []
  col  = df[df.columns[column_id]]
  for v in col.unique():
    data.append((v, df[col == v].shape[0]))

  if custom_sort is not None:
    data = sorted(data, key=lambda x: custom_sort(x[0]))

  return pd.DataFrame({label: [x[1] for x in data]},
                      index = [x[0] for x in data])

def get_data_multiple(column_id, label, custom_sort):
  col  = df[df.columns[column_id]]
  data = {}

  for v in col:
    for s in v.split(';'):
      if s not in data.keys():
        data[s] = 1
      else:
        data[s] += 1

  sets = []
  for v in data.keys():
    sets.append((v, data[v]))
  sets.reverse()


  if custom_sort is not None:
    sets = sorted(sets, key=lambda x: custom_sort(x[0]))

  return pd.DataFrame({label: [x[1] for x in sets]},
                      index = [x[0] for x in sets])

def vis_pie(column_id, label, multiple = False, colours = None, custom_sort = None):
  getter = get_data_multiple if multiple else get_data_basic
  frame  = getter(column_id, label, custom_sort)
  plot   = frame.plot.pie(y=label,
                          autopct='%1.0f%%',
                          title=df.columns[column_id],
                          colors=colours,
                          labeldistance = None,
                          counterclock = False,
                          fontsize=8)
  plot.legend(frame.index, bbox_to_anchor=(1.05, 1), loc="upper left")
  return plot

def vis_bar(column_id, label, vertical = False, colours = None, multiple = False, custom_sort = None):
  getter  = get_data_multiple if multiple else get_data_basic
  frame   = getter(column_id, label, custom_sort)
  plotter = frame.plot.bar if vertical else frame.plot.barh
  plot    = plotter(y=label,
                    title=df.columns[column_id],
                    align='edge',
                    color=colours,
                    fontsize=8)
  plot.legend([label], bbox_to_anchor=(1.05, 1), loc="upper left")
  return plot

### ΚΥΡΙΩΣ ΣΩΜΑ

def main(win):
  win.nodelay(True)

  curses.start_color()
  curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
  curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)

  choice = selector(win)

  win.clear()

  # Κλήση συνάρτησης οπτικοποίησης
  plot = vis_func_by_id(choice)()
  fig  = plot.get_figure()

  savename = save(win, choice).strip()
  fig.savefig(savename, bbox_inches="tight")
  exit(0)

# Παράθυρο επιλογής ερώτησης
def selector(win):
  choice_confirmed = False
  current_choice   = 0

  def print_choice():
    win.clear()
    win.addstr(1, 0, "Επιλέξτε μια ερώτηση:".center(curses.COLS))
    display  = "<"
    display += " " *3
    display += vis_name_by_id(current_choice)
    display += " " *3
    display += ">"
    win.addstr(3, 0, display.center(curses.COLS), curses.color_pair(1) | curses.A_BOLD)
    win.addstr(6, 0, "Χρησιμοποιήστε τα πλήκτρα με τα βελάκια για αλλαγή ερώτησης.".center(curses.COLS))
    win.addstr(7, 0, "Πατήστε ΚΕΝΟ για να επιβεβαιώσετε την επιλογή σας".center(curses.COLS))
    win.addstr(8, 0, "ή Q για έξοδο.".center(curses.COLS))

  print_choice()

  while not choice_confirmed:
    key = None
    try:
      key = win.getkey()
    except: # no input
      pass

    if key is None:
      continue

    if key == "KEY_LEFT" or key == "KEY_UP":
      current_choice -=1
      if(current_choice < 0):
        current_choice = len(VISUALIZEABLE)-1
      print_choice()

    elif key == "KEY_RIGHT" or key == "KEY_DOWN":
      current_choice +=1
      if(current_choice > len(VISUALIZEABLE)-1):
        current_choice = 0
      print_choice()

    elif key == " ":
      choice_confirmed = True

    elif key.lower() == "q":
      exit(0)

  return current_choice


# Παράθυρο επιλογής προορισμού αποθήκευσης
def save(win, choice):
  win.clear()
  win.addstr(1, 0, "Επιλέχθηκε οπτικοποίηση για την ερώτηση:", curses.A_UNDERLINE | curses.A_BOLD)
  win.addstr(2, 4, vis_name_by_id(choice))

  SAVEPROMPT="Αποθήκευση γραφήματος ως: "
  win.addstr(4, 0, SAVEPROMPT, curses.color_pair(2))
  win.addstr(6, 0, "Πατήστε ENTER ή Ctrl+G για αποθήκευση".center(curses.COLS))

  lineedit = curses.newwin(1, (curses.COLS - len(SAVEPROMPT)), 4, len(SAVEPROMPT))
  lineedit.bkgd(' ', curses.color_pair(2))

  win.refresh()
  textbox  = Textbox(lineedit)
  textbox.edit()

  return textbox.gather()

if __name__ == '__main__':
  curses.wrapper(main)
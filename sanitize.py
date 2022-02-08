#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from _datacore import df, NaN, check_data
from _format   import *
from random    import randrange

check_data(True)

# Τυχαία δειγματοληψία
df = df.sample(frac = 1)

# Αριθμοί, όχι ημερομηνίες
df.rename(columns = {df.columns[0]: "Α/Α"}, inplace = True)
existing = []
for i, r in enumerate(df[df.columns[0]]):
  rand = None
  while rand is None or rand in existing:
    rand = randrange(10000, 99999)
    df.loc[i, df.columns[0]] = rand
  existing.append(rand)

# Ερωτήσεις
QGENDER = df.columns[1]
QAGE    = df.columns[2]
QEDU    = df.columns[3]

Q3_1    = df.columns[22]
Q3_2    = df.columns[23:27]
Q3_3    = df.columns[27]

Q3_2_1  = Q3_2[0]
Q3_2_2  = Q3_2[1]
Q3_2_3  = Q3_2[2]
Q3_2_4  = Q3_2[3]


### ΕΠΑΝΑΧΡΗΣΙΜΟΠΟΙΗΣΙΜΕΣ ΣΥΝΑΡΤΗΣΕΙΣ

# Εντοπισμός άκυρων απαντήσεων στις 3.2 και 3.3
def άκυρες_απαντήσεις_3_1(δεδομένα):
  ret = []
  for i in δεδομένα[Q3_1].index:
    if(δεδομένα[Q3_1][i] == "Όχι"):
      valid = (δεδομένα[Q3_2_1].isnull()[i] and δεδομένα[Q3_2_2].isnull()[i] and δεδομένα[Q3_2_3].isnull()[i] and δεδομένα[Q3_2_4].isnull()[i] and δεδομένα[Q3_3].isnull()[i])
      if not valid:
        ret.append(i)
  return ret

# Προσδιορισμός αναλογίας φύλων
def αναλογία_φύλων(δεδομένα):
  ret = {}
  for gender in δεδομένα[QGENDER].unique():
    ret[gender] = (δεδομένα[QGENDER] == gender).sum()

  return ret

def αναλογία_εκπαίδευσης(δεδομένα):
  ret = {}
  for edu in δεδομένα[QEDU].unique():
    ret[edu] = (δεδομένα[QEDU] == edu).sum()

  return ret

def αναλογία_ηλικίας(δεδομένα):
  ret = {}
  for age in δεδομένα[QAGE].unique():
    ret[age] = (δεδομένα[QAGE] == age).sum()

  return ret

# Πίνακας αναλογίας
def πίνακας_αναλογίας(αναλογία, είδους):
  print(underlined("Αναλογία {}:".format(είδους), '-'))

  amax = max(αναλογία.values())
  atot = sum(αναλογία.values())

  for val in αναλογία.keys():
    perc = 100 * αναλογία[val] / atot # Ποσοστό στο σύνολο

    if(αναλογία[val] == amax):
      # Μέγιστη τιμή
      diff = "ΜΕΓΙΣΤΟ"
    else:
      # Ποσοστό διαφοράς από τη μέγιστη τιμή
      diff = "{:6.2f}%".format(perc - (100 * amax / atot))

    print("{}\t{}\t{:6.2f}%\t\t{}".format(val.ljust(40), αναλογία[val], perc, diff))

  print("_" * 80)
  print("{}\t{}\t{:6.2f}%".format("Σύνολο:".ljust(40), atot, 100))

# Αναφορά
def αναφορά(δεδομένα, τίτλος):
  print("\n"+underlined(τίτλος.upper())+"\n")

  print(underlined("Άτομα που συμπλήρωσαν τις 3.2 και 3.3 χωρίς να έχουν απαντήσει ΝΑΙ στην 3.1:", '-'))
  print("\t{}\n".format(len(άκυρες_απαντήσεις_3_1(δεδομένα))))

  πίνακας_αναλογίας(αναλογία_φύλων(δεδομένα), "φύλων")
  print()

  πίνακας_αναλογίας(αναλογία_ηλικίας(δεδομένα), "ηλικίας")
  print()

  πίνακας_αναλογίας(αναλογία_εκπαίδευσης(δεδομένα), "εκπαίδευσης")
  print()


### ΚΥΡΙΩΣ ΣΩΜΑ

if __name__ == '__main__':
  save_screen()
  clear_screen()

  αναφορά(df, "αναφορα υπαρχοντων δεδομενων")

  pause()

  # Θα δουλέψουμε με ένα αντίγραφο τώρα
  nf = df.copy()

  clear_screen()
  print("*" * 80)

  # Κάθαρση των λάθως απαντήσεων στις 3.2 και 3.3
  wrong = άκυρες_απαντήσεις_3_1(nf)
  for n in wrong:
    nf.loc[n, Q3_2_1] = NaN
    nf.loc[n, Q3_2_2] = NaN
    nf.loc[n, Q3_2_3] = NaN
    nf.loc[n, Q3_2_4] = NaN
    nf.loc[n, Q3_3]   = NaN
  print("Διορθώθηκαν απατήσεις στις 3.2 και 3.3:")
  print("\t{}".format(len(wrong)))
  del wrong

  print()

  # Συγχώνευση 'Πανεπιστήμιο' με 'Πανεπιστήμιο ΑΕΙ/ΑΤΕΙ' (επανάληψη)
  subst = nf[nf[QEDU] == "Πανεπιστήμιο"].index
  for i in subst:
    nf.loc[i, QEDU] = "Πανεπιστήμιο ΑΕΙ/ΑΤΕΙ"

  print("Διορθώθηκαν διπλότυπες κατηγορίες:")
  print("\t{}".format(subst.size))

  print()

  # Αφαίρεση ανηλίκων
  underage = nf[nf[QAGE] == "Κάτω των 18"].shape[0]
  nf = nf[nf[QAGE] != "Κάτω των 18"]
  print("Αφαιρέθηκαν {} ανήλικοι.".format(underage))

  print()

  # Εξισορρόπιση φύλων
  genders = αναλογία_φύλων(nf)
  diff = genders['Θήλυ'] - genders['Άρρεν']

  if diff == 0:
    print("Δεν χρειάζεται εξισορρόπηση για τα φύλα.")
  else:
    g1     = ( 'Θήλυ' if diff > 0 else 'Άρρεν' )
    g2     = ( 'Θήλυ' if diff < 0 else 'Άρρεν' )

    edu    = αναλογία_εκπαίδευσης(nf)
    edurm  = max(edu, key=edu.get)

    age    = αναλογία_ηλικίας(nf)
    agerm  = max(age, key=age.get)

    # Εντοπισμός κυρίαρχης ομάδας ερωτηματολογίων προς αφαίρεση με βάση φύλο, ηλικία και εκπαίδευση
    match  = nf[((nf[QGENDER] == g1) & (nf[QAGE] == agerm) & (nf[QEDU] == edurm))]

    # Υπολογισμός αριθμού ερωτηματολογίων προς απόρριψη
    matchc = match.shape[0]
    rm     = matchc if matchc < diff else diff
    if nf.shape[0] - rm < 100:
      # Δεν θέλουμε να πάμε κάτω από 100
      rm -= 100 - (nf.shape[0] - rm)

    # Οριοθέτηση ερωτηματολογίων προς απόρριψη
    match  = match[:rm]

    # Απόρριψη ερωτηματολογίων
    col0 = nf.columns[0]
    for i in match[col0]:
      nf = nf[nf[col0] != i]

    print("Αφαιρέθηκαν άτομα φύλου {} με ηλικία {} και εκπαίδευση {}:".format(g1, agerm, edurm))
    print("\t{} (από τα υπάρχοντα {})".format(rm, matchc))

  print("*" * 80)

  αναφορά(nf, "αναφορα νεων δεδομενων")

  savename = ""
  while not savename:
    try:
      savename = input("Δώστε ένα όνομα στο νέο αρχείο: ")
    except KeyboardInterrupt:
      print("\rΗ αποθήκευση ακυρώθηκε.")
      exit(0)

  saverror = False
  try:
    nf.to_csv(savename, index=False)
  except:
    saverror = True

  clear_screen()
  restore_screen()
  if saverror:
    print("Η αποθήκευση στο αρχείο {} απέτυχε.".format(savename))
  else:
    print("Αποθηκεύτηκε στο αρχείο {}.".format(savename))
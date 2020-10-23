# code om punten te tellen
# Punten Module
# Spelers Module
# @Author Damian
# code om de levens te berekennen en weer te geven
# @Aghead_Bilal
# je begint met 3 levens standard

#
target = True
targetIsHit = False
Levens = 3


# Punten
start_punten = 0
punten = 0
eind_punten = start_punten + punten


speler = input("Voer hier uw nickname in: ")
print(speler + " Get Ready !" )


import time

# define the countdown func.
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1

# na het voltooien van de loop, printen we "Fire in the hole" om te weer te geven dat het eind van de countdown is
    print('Missed Shot')

# input time in seconds
t = input("Enter the time in seconds to start the game: ")

# loop om de levens te bewerken als de target niet geraakt is
while target == True and Levens != 0:
    if targetIsHit == False:
        countdown(int(t))
        print(f"Levens:{Levens - 1}")
        Levens -= 1
    else: targetIsHit = True
    punten + 1
# Punten toevoegen waneer sensor afgaat


print("Totaal Punten:")
print(eind_punten)









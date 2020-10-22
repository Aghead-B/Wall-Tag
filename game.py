# code om de levens te berekennen en weer te geven
# @Aghead_Bilal
target = True
targetIsHit = False
# je begint met 3 levens standard
Levens = 3

# import the time module
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
    print('Fire not in the hole!!')


# input time in seconds
t = input("Enter the time in seconds: ")

# loop om de levens te bewerken als de target niet geraakt is
while target == True and Levens != 0:
    if targetIsHit == False:
        countdown(int(t))
        print(f"Levens:{Levens - 1}")
        Levens -= 1































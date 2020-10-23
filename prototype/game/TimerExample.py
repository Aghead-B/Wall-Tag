import time

timeElapsed = 0
interval = 100
while True:
    if timeElapsed >= 2000:
        break
    if timeElapsed >= 1000:
        timeElapsed = 0
    timeElapsed += interval
    time.sleep(interval / 1000)
    print(timeElapsed)

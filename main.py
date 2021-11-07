from pynput.keyboard import Key, Listener
import sys
import os
import time
from threading import Thread

counter = 0
bot_number = 0
bot_price = 10

# Get OS
clear = ""
os_ = sys.platform
if os_ == "linux" or os_ == "darwin":
    clear = "clear"
elif os_ == "win32":
    clear = "cls"


def release(key):
    global counter, t, bot_number, bot_price

    # Calculate the bot price depending on the number of bots
    bot_price = 10 + (round(bot_number/5, 0)*10)

    if key == Key.space:
        # Add a point for every space clicked
        counter += 1
        return counter
    elif key == Key.esc:
        # Exit
        display.terminate()
        t.join()
        quit(0)

    try:
        if key.char == 'b':
            # Buy a bot
            if counter >= bot_price:
                bot_number += 1
                counter -= bot_price
            else:
                print("Not enough points")
    except AttributeError:
        pass

# Create a terminatable thread that shows the counter variable
class display_class:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def display(self):
        while self._running:
            global counter, bot_number, bot_price

            os.system(clear)

            counter = round(counter + int(bot_number)/10, 1)
            str_counter = str(int(round(counter)))
            if counter >= 1000:
                str_counter = str(round(counter/1000)) + "K"

            print(str_counter)

            print('Buy a bot with "b"')
            print("Bot price: " + str(int(bot_price)))
            print("Bot clicks at the rate : 1 per sec")
            print("Number of active bots: " + str(bot_number))
            time.sleep(0.1)

display = display_class()
t = Thread(target = display.display)
t.start()

# Listen for key presses
with Listener(on_release=release) as listener:
    listener.join()

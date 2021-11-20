from pynput.keyboard import Key, Listener
import sys
import os
import time
from threading import Thread
import json

save_file = "spc-clicker.sav"

space_counter = 0

bot_number = 0
bot_price = 10

click_multi_number = 0
click_multi_price = 100

# Load from the save file
if os.path.exists(save_file):
    with open(save_file, "r") as f:
        # Convert the JSON to a dictionary
        a = f.read()
        dict = json.loads(a)
        # Asign all of the variables with the info from the file
        space_counter = float(dict["space"])
        bot_number = int(dict["bot_num"])
        bot_price = int(dict["bot_price"])
        click_multi_number = int(dict["click_multi"])
        click_multi_price = int(dict["click_multi_price"])

def save(space_counter, bot_number, bot_price, click_multi_number, click_multi_price):
    # Write the regular info into the file
    with open(save_file, "w") as f:
        write_text = f"space {space_counter}\nbot_num {bot_number}\nbot_price {bot_price}\nclick_multi {click_multi_number}\nclick_multi_price {click_multi_price}"
        f.write(write_text)
    # Read what was previously read and convert it to JSON
    dict = {}
    with open(save_file, "r") as f:
        for line in f:
            a, b = line.strip().split(None, 1)
            dict[a] = b.strip()
    # Write the JSON to the file, removing the original text in it
    with open(save_file, "w") as f:
        json.dump(dict, f, indent = 4, sort_keys = False)


# Get OS
clear = ""
os_ = sys.platform
if os_ == "linux" or os_ == "darwin":
    clear = "clear"
elif os_ == "win32":
    clear = "cls"


def release(key):
    global space_counter, t, bot_number, bot_price, click_multi_price, click_multi_number

    # Calculate the bot price depending on the number of bots
    # Increase the price every 5 bots
    bot_price = 10 + (round(bot_number/5)*30)
    # Calculate the click multiplier
    click_multi_price = click_multi_number * 1000
    if click_multi_price == 0:
        click_multi_price = 100

    if key == Key.space:
        # Add a point for every space clicked
        space_counter += click_multi_number*5
        if click_multi_number == 0:
            space_counter+=1
        return space_counter
    elif key == Key.esc:
        # Exit
        save(space_counter, bot_number, bot_price, click_multi_number, click_multi_price)
        display.terminate()
        t.join()
        sys.exit("Exit")

    try:
        if key.char == 'b':
            # Buy a bot
            if space_counter >= bot_price:
                bot_number += 1
                space_counter -= bot_price
            else:
                print("Not enough points")
        if key.char == 'n':
            # Buy a click multiplier
            if space_counter >= click_multi_price:
                click_multi_number += 1
                space_counter -= click_multi_price
            else:
                print("Not enough points")

    except AttributeError:
        pass

# Create a terminatable thread that shows the space_counter variable
class display_class:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def display(self):
        while self._running:
            global space_counter, bot_number, bot_price, click_multi_number, click_multi_price

            os.system(clear)
            # Add points based on the amount bots
            space_counter = round(space_counter + int(bot_number)/10, 1)

            str_space_counter = str(int(round(space_counter)))
            if space_counter >= 1000:
                str_space_counter = str(round(space_counter/1000, 1)) + "K"

            print(str_space_counter)

            print('\nBuy a bot with "b"')
            print("Bot price: " + str(int(bot_price)))
            print("Bot clicks at the rate : 1 per sec")
            print(f"All bots together click at the rate: {bot_number} per sec")

            print('\nBuy a click multiplier with "n"')
            print("Click multiplier price: " + str(int(click_multi_price)))
            click = click_multi_number*5
            if click == 0:
                click = 1
            print(f"1 click = {str(click)} points")

            time.sleep(0.1)

display = display_class()
t = Thread(target = display.display)
t.start()

# Listen for key presses
with Listener(on_release=release) as listener:
    listener.join()

# varying temperature of one thermode
from classes_thermodes import Thermode
import time
import numpy as np

if __name__ == "__main__":

    previous_temp = 33

    while True:
        temp = Thermode()
        target_temp = input("\n What is the target temperature?")

        temp.ramp(previous_temp, float(target_temp))

        temp.IO_thermode("ai8", "ao0")

        previous_temp = float(target_temp)

        while True:
            decision = input(
                "\n Do we want to keep playing with the thermodes? (Y/n)  "
            )
            if decision in ("Y", "n"):
                if decision == "Y":
                    break
                elif decision == "n":
                    print("WE ARE DONE!")
                    exit()
            else:
                print("\n Only Y and n are valid responses")
                continue

            continue

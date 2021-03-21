#!/usr/bin/env python3

import modules.module_loader as ml
import tools.sklearn_sims as sk
import time

def main():
    classes = ml.class_builder()
#    color_test(classes)
#    on_off_test(classes)
    bright_test(classes)

def color_test(classes):
    colors = [
            "red",
            "orange",
            "yellow",
            "springgreen",
            "green",
            "turquoise",
            "cyan",
            "ocean",
            "blue",
            "violet",
            "magenta",
            "raspberry"
            ]

    for i in colors:
        sk.compare_command("turn the flux lightbulb color to "+i, classes)
        time.sleep(2)

def on_off_test(classes):
    #sk.compare_command("turn the flux light bulb off", classes)
    #time.sleep(2)
    sk.compare_command("turn the flux light bulb on", classes)

def bright_test(classes):
    sk.compare_command("set the brightness of the flux light bulb to ten percent", classes)

if __name__ == "__main__":
    main()

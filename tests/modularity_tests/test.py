#!/usr/bin/env python3
import modules.module_loader as ml
import tools.sklearn_sims as sk
import time

def main():
    classes = ml.class_builder()
    #lmp_test(classes)
    #sw_test(classes)
    #timer_test(classes)
    weather_test(classes)

def lmp_test(classes): #test for local music player
    sk.compare_command("play the song country roads", classes)
    time.sleep(3)
    sk.compare_command("stop playing music", classes)
    time.sleep(3)
    sk.compare_command("continue playing music", classes)
    time.sleep(3)
    sk.compare_command("stop playing music", classes)

def sw_test(classes): #test for stopwatch
    sk.compare_command("setup a stopwatch", classes)
    time.sleep(3)
    sk.compare_command("end the stopwatch", classes)

def timer_test(classes): #test for timer
    sk.compare_command("set a timer for 3 seconds", classes)
    time.sleep(5)

def weather_test(classes): #test for weather feature
    sk.compare_command("what's the weather in", classes)
    sk.compare_command("what's the weather", classes)
    sk.compare_command("what's the weather in brighton", classes)


if __name__ == "__main__":
    main()

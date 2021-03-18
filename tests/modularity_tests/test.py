#!/usr/bin/env python3
import modules.module_loader as ml
import tools.sklearn_sims as sk
import time

def main():
    classes = ml.class_builder()
    lmp_test(classes)
    #sw_test(classes)
    #timer_test(classes)
    #weather_test(classes)
    #yt_music_test(classes)

def lmp_test(classes): #test for local music player
    sk.compare_command("play the song swear", classes)
    time.sleep(3)
    sk.compare_command("you must stop playing music", classes)
    time.sleep(3)
    sk.compare_command("unpause the music", classes)
    time.sleep(3)
    sk.compare_command("the music must stop", classes)
    time.sleep(3)
    sk.compare_command("play the song domino line by john denver", classes)
    time.sleep(3)

def sw_test(classes): #test for stopwatch
    sk.compare_command("setup a stopwatch", classes)
    time.sleep(3)
    sk.compare_command("end the stopwatch", classes)
    sk.compare_command("terminate the stopwatch", classes)


def timer_test(classes): #test for timer
    sk.compare_command("setup a timer for 3 seconds", classes)
    time.sleep(5)

def weather_test(classes): #test for weather feature
    sk.compare_command("lookup the weather in", classes)
    sk.compare_command("get the weather", classes)
    sk.compare_command("get the weather for brighton", classes)

def yt_music_test(classes):
    sk.compare_command("using youtube play the song swear by casio pea", classes)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import modules.module_loader as ml
import tools.sklearn_sims as sk
import flux_test as flux
import plug_test as plug
import clock_test as clock
import DOORS.main as mn
import time

def main():
    classes = ml.class_builder()
    lmp_test(classes)
    sw_test(classes)
    timer_test(classes)
    weather_test(classes)
    yt_music_test(classes)
    flux.tests(classes)
    plug.tests(classes)
    clock.tests(classes)
    secret_test(classes)


def lmp_test(classes): #test for local music player
    sentences = [
                "play the song swear",
                "you must stop playing music",
                "unpause the music",
                "the music must stop",
                "play the song domino line by john denver",
            ]
    run_stuff(sentences, classes, 3)
        
def sw_test(classes): #test for stopwatch
    sent = [
                "setup a stopwatch",
                "end the stopwatch",
                "terminate the stopwatch",
        ]
    run_stuff(sent, classes, 2)
    
def timer_test(classes): #test for timer
    sent = [
                "setup a timer for 3 seconds",
        ]
    run_stuff(sent, classes, 5)

def weather_test(classes): #test for weather feature
    sent = [
                "lookup the weather in",
                "get the weather",
                "get the weather for brighton",
        ]
    run_stuff(sent, classes, 1)

def yt_music_test(classes):
    sent = [
                "using youtube play the song swear by casio pea",
        ]
    run_stuff(sent, classes, 0)

def secret_test(classes):
    sent = [
                "who is jj geeks",
        ]
    run_stuff(sent, classes, 0)

def run_stuff(sentences, classes, delay):
    for i in sentences:
        msg, func, mod = sk.compare_command(i, classes)
        print(msg)
        if func: #we got a function back
                if mod in classes.keys(): #classes functions should manipulate themselves
                    func(classes[mod])
                else:
                    func()
        time.sleep(delay)


if __name__ == "__main__":
    main()

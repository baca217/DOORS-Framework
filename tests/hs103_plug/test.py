#!/usr/bin/env python3
import time
import modules.module_loader as ml
import tools.sklearn_sims as sk

def main():
    classes = ml.class_builder()
    on_test(classes)
    time.sleep(3)
    off_test(classes)
    time.sleep(3)
    info_test(classes)

def on_test(classes):
    sk.compare_command("turn on the power plug", classes)

def off_test(classes):
    sk.compare_command("turn off the power plug", classes)

def info_test(classes):
    sk.compare_command("is the power plug on", classes)

if __name__ == "__main__":
    main()

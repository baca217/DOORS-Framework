#!/usr/bin/env python3

import modules.module_loader as ml
import tools.sklearn_sims as sk
import time

def main():
    classes = ml.class_builder()
    flux_test(classes)

def flux_test(classes):
    sk.compare_command("turn the flux lightbulb color to cyan", classes)

if __name__ == "__main__":
    main()

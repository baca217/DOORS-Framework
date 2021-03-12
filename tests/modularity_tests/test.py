#!/usr/bin/env python3
import modules.module_loader as ml
import tools.sklearn_sims as sk
import time

def main():
    sk.compare_command("play the song country roads")
    time.sleep(3)
    sk.compare_command("stop playing music")
    sk.compare_command("continue playing music")
    time.sleep(3)
    sk.compare_command("stop playing music")
if __name__ == "__main__":
    main()

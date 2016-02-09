#!/usr/bin/env python3
from motherrussia import MotherRussia
import argparse

def play_intro():
    string = '''
    Ladies and gentlemen, this is ... 
    ________       __________         
    ___  __ \___  ___  /___(_)______ 
    __  /_/ /  / / /  __/_  /__  __ \\
    _  ____// /_/ // /_ _  / _  / / /
    /_/     \__,_/ \__/ /_/  /_/ /_/ 
    '''
    print(string)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--timeout', type=float)
    args = parser.parse_args()

    if not args.debug:
        play_intro()

    with MotherRussia(args.debug, args.timeout) as mother:
        mother.init()
        mother.run()

if __name__ == "__main__":
    main()

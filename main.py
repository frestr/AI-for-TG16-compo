#!/usr/bin/env python3
from motherrussia import MotherRussia
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-t', '--timeout', type=float)
    args = parser.parse_args()

    with MotherRussia(args.debug, args.timeout) as mother:
        mother.init()
        mother.run()

if __name__ == "__main__":
    main()

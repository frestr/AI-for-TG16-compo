#!/usr/bin/env python3
from motherrussia import MotherRussia

def main():
    with MotherRussia() as mother:
        mother.init()
        mother.run()
        
if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from motherrussia import MotherRussia

def main():
    mother = MotherRussia()
    try:
        mother.init()
        mother.run()
    except KeyboardInterrupt:
        print('Received keyboard interrupt')
    except Exception as e:
        print('Exception: ', e)
    finally:
        print('Attempting to clean up...')
        mother.clean()

if __name__ == "__main__":
    main()

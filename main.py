#!/usr/bin/env python3
from socketHandler import socketHandler
import json

def main():
    connector = socketHandler()
    connector.connect()
    connector.send_data('NAME bob\n')

    while True:
        data = json.loads(connector.poll_data())
        print(data)

if __name__ == "__main__": 
    main()

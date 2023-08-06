# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 18:40:24 2021

@author: seaty
"""
nato_spelling = {
    "a": "Alpha",
    "b": "Bravo",
    "c": "Charlie",
    "d": "Delta",
    "e": "Echo",
    "f": "Foxtrot",
    "g": "Golf",
    "h": "Hotel",
    "i": "India",
    "j": "Juliet",
    "k": "Kilo",
    "l": "Lima",
    "m": "Mike",
    "n": "November",
    "o": "Oscar",
    "p": "Papa",
    "q": "Quebec",
    "r": "Romeo",
    "s": "Sierra",
    "t": "Tango",
    "u": "Uniform",
    "v": "Victor",
    "w": "Whisky",
    "x": "X-ray",
    "y": "Yankee",
    "z": "Zulu",
}

import argparse
import sys

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument('inputString', nargs='?', default="", help="Optional argument - if not provided, the program will prompt for a string.")
    return parser.parse_args()
    
    
def main():
    inputString = parseArguments().inputString
    while True:
        if inputString == "":
            inputString = input("Enter a String to be converted into the NATO Alphabet, or type exit:\n")
        inputString = inputString.lower()
        if inputString == "exit":
            sys.exit()
        for letter in inputString:
            print(letter + "\t" + nato_spelling.get(letter, letter))
        inputString = ""
            

if __name__ == "__main__":
    main()
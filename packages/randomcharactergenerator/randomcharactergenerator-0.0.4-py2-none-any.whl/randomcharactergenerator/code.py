import random


def rand_code(characters=5):
    """
    Returns a random string containing alphabets and numbers
    Default number of characters: 5
    """
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                 't', 'u', 'v', 'w', 'x', 'y', 'r']

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    code_list = [alphabets, numbers]
    i = 0
    code = ''
    while i < characters:
        choice = random.choice(code_list)
        code = code + str(random.choice(choice))
        i += 1
    return code


def alphabet_code(characters=5):
    alphabets = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
                 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a',
                 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                 't', 'u', 'v', 'w', 'x', 'y', 'r']
    """
    Returns a string containing random alphabets (Both lower and upper case)
    Default number of characters: 5
    """
    i = 0
    code = ''
    while i < characters:
        code = code + str(random.choice(alphabets))
        i += 1
    return code


def number_code(characters=5):
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    """
    Returns a string containing random numbers
    Default number of characters: 5
    """
    i = 0
    code = ''
    while i < characters:
        code = code + str(random.choice(numbers))
        i += 1
    return code


def module_help():
    """
    Help function for this library
    """
    print("Hi! Welcome to the help")
    while True:
        inpt = input("""
For help about rand_code() function, enter '1'. 
For help about 'number_code()' function, enter '2'. 
For help about 'alphabet_code()' function, enter '3'. 
For general help, enter '4. 
To exit, enter 'exit'.""")
        if str(inpt) == '1':
            print("""
FUNCTION: rand_code()
PARAMETERS: characters - number of characters for the string - option - default number of characters is 5
USAGE: 

import randomcharactergenerator
string = randomcharactergenerator.rand_code()
print(string)

The above code will print out a random string containing both numbers and letters.
""")
        elif str(inpt) == '2':
            print("""
FUNCTION: number_code()
PARAMETERS: characters - number of characters for the string - option - default number of characters is 5
USAGE: 

import randomcharactergenerator
string = randomcharactergenerator.number_code()
print(string)

The above code will print out a random string containing numbers only.
            """)
        elif str(inpt) == '3':
            print("""
FUNCTION: rand_code()
PARAMETERS: characters - number of characters for the string - option - default number of characters is 5
USAGE: 

import randomcharactergenerator
string = randomcharactergenerator.alphabet_code()
print(string)

The above code will print out a random string containing letters only (both upper and lower case).
            """)
        elif str(inpt) == '4':
            print("""
The library contains 4 functions: rand_code(), alphabet_code(), number_code() and module_help()
rand_code() generates a string with both alphabets and numbers
alphabet_code() generates a string with only alphabets
number_code() generates a string with only numbers
module_help() shows the help for this library""")

        elif str(inpt) == 'exit':
            quit()
        else:
            print("Sorry. Don't know that")

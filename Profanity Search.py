"""
FileName: Profanity Search.py
Version: 1.0
Author: Andrew Racine
Date of Creation: 12/8/2015
Date of Last modification 12/8/2015
Synopsis: This program prompts the user for a list of URLs. It then iterates through the list and determines whether
each URL in the list contains profanity or not. If the URL is found to contain profanity it then prints it out.
"""

import urllib2
import sys
import time
from bs4 import BeautifulSoup


def get_webpage(webpage):
    """
    This function takes in a URL and returns the body text contained in the processed URL
    :param webpage: A URL
    :return: Body of Text
    """
    response = urllib2.urlopen(webpage)
    html = response.read()
    try:
        soup = BeautifulSoup(html, 'html.parser')
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text
    except:
        time.sleep(1)
        print("The following line could not be parsed: {}".format(webpage))
        print("---------------------------------------------------------------------------")


def get_file():
    """
    Safely prompts for and returns a file
    :return: File with list of URLs
    """
    try:
        URL_list = open(raw_input("Enter filename: "), 'r')
        return URL_list
    except IOError:
        print("No file with that name. Please try again.")
        return get_file()


def check_website():
    """
    This function prompts the user for a file of URLs to iterate through. It then checks to see if any contain
    profanity and prints the results at the end.
    :return: None
    """

    #  Opens profanity file
    profanity_file = open('profanity.txt', 'r')
    lst_of_profanity = []
    for line in profanity_file:
        line = line.strip()
        lst_of_profanity.append(line)
    profanity_file.close()

    # Prompts for URL file list
    text = get_file()
    print("The following articles contain profanity.")
    print("---------------------------------------------------------------------------")
    for line in text:
        # Grab URL from list
        html = get_webpage(line)

        if html is not None:
            #  Initializes variables
            has_profanity = False
            lst_of_used_profanity = []
            profanity_count = 0

            #  Checks URL for profanity
            for word in html.split():
                word = word.lower()
                if word in lst_of_profanity:
                    if word not in lst_of_used_profanity:
                        profanity_count += 1
                        lst_of_used_profanity.append(word)
                    has_profanity = True
            if has_profanity:
                # Prints results
                print("URL: {}".format(line))
                print("Profanity: {}".format(has_profanity))
                print("Count: {}".format(profanity_count))
                print("Lst: {}".format(lst_of_used_profanity))
                print("---------------------------------------------------------------------------")
    print("Search is complete.")


def main():
    check_website()
    response = raw_input("Do you want to check another URL list? Y/N: ")
    response = response.capitalize()
    if response == "Y":
        main()
    elif response == "N":
        sys.exit()
    else:
        print("Incorrect input. Program will now shutdown.")
        sys.exit()

#  User Warning
print("Please ensure the following: ")
print("File is in same directory as program, or that full path is provided.")
print("File contains only website URLs, one per line, and there is no space between website URLs.")
main()
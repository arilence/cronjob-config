"""---------------------------------------------------------------------------------------
--      SOURCE FILE:            cron.py - A Simple Cron File Generator
--
--      PROGRAM:                cron
--
--      FUNCTIONS:              __init__(self)
--                              inputAnswer(self, prompt, validation)
--                              validateFrequency(self, frequency)
--                              validateEmail(self, email)
--                              validateFile(self, fileLocation)
--                              createCronFile(self, frequency, email, fileLocation)
--
--      DATE:                   October 11, 2016
--
--      REVISIONS:              (Date and Description)
--                              October 12, 2016
--                              Modified the input to accept command line arguments
--
--      DESIGNERS:              Anthony Smith
--
--      PROGRAMMERS:            Anthony Smith
--
--      NOTES:
--      The program will generate a cronjob to send an email with an attached file
--      at every specified interval. The program reads command line arguments or
--      prompts the user for the arguments unspecified.
--------------------------------------------------------------------------------------"""
import sys, re, argparse
from pathlib import Path
from enum import Enum

class Shell:
    def __init__(self, args):
        ## Enter cronjob frequency
        if args.freq and self.validateFrequency(args.freq):
            frequency = args.freq
        else:
            frequency = self.inputAnswer('Frequency of the cronjob (* * * * *): ', self.validateFrequency)

        ## Enter email address
        if args.email and self.validateEmail(args.email):
            email = args.email
        else:
            email = self.inputAnswer('Recipient email (test@example.com): ', self.validateEmail)

        ## Enter file location
        if args.file and self.validateFile(args.file):
            fileLoc = args.file
        else:
            fileLoc = self.inputAnswer('File to attach to the email (/var/root): ', self.validateFile)

        ## Create cronfile
        if (self.createCronFile(frequency, email, fileLoc)):
            print('Cronfile create successfully')
        else:
            print('Hmm... looks like something failed, please try again')

    def inputAnswer(self, prompt, validation):
        while True:
            value = input(prompt)
            if validation(value) == True:
                return value

    def validateFrequency(self, frequency):
        entryArray = frequency.split()
        if len(entryArray) == 5:
            return True
        else:
            print('\nInvalid Frequency')
            return False

    def validateEmail(self, email):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if pattern.match(email):
            return True
        else:
            print('\nInvalid Email Address')
            return False

    def validateFile(self, fileLocation):
        theFile = Path(fileLocation)
        if theFile.is_file():
            return True
        else:
            print('\nInvalid File Location')
            return False

    def createCronFile(self, frequency, email, fileLocation):
        template = '{} echo “Here is a requested file” | mail -s “Cron Job” -a {} {}'.format(frequency, fileLocation, email)

        _file = open('.temp-cron', 'w+')
        _file.write(template)
        _file.close()
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--freq', help='How often the cronjob runs')
    parser.add_argument('--email', help='Address to send an email to')
    parser.add_argument('--file', help='Location of a file to attach to an email')
    args = parser.parse_args()

    shell = Shell(args)

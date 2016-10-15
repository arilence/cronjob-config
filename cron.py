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
--                              October 15, 2016
--                              Fix cronjob importing from file
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
import sys, re, argparse, subprocess, os
from pathlib import Path
from enum import Enum

class Shell:

    """---------------------------------------------------------------------------------------
    -- FUNCTION:   __init__
    -- DATE:       15/10/2016
    -- REVISIONS:  (V1.0)
    -- DESIGNER:   Anthony Smith
    -- PROGRAMMER: Anthony Smith
    -- INPUT:      args : object that holds command line arguments
    -- RETURNS:    None
    --
    -- NOTES:
    -- Prompts the user for the cronjob frequency, recipients email address, and file
    -- location. Then attempts to create a cronjob from the user's input.
    --------------------------------------------------------------------------------------"""
    def __init__(self, args):
        ## Enter cronjob frequency
        if args.freq and self.validateFrequency(args.freq):
            frequency = args.freq
        else:
            frequency = self.inputAnswer('Frequency of the cronjob (eg: * * * * *): ', self.validateFrequency)

        ## Enter email address
        if args.email and self.validateEmail(args.email):
            email = args.email
        else:
            email = self.inputAnswer('Recipient email: ', self.validateEmail)

        ## Enter file location
        if args.file and self.validateFile(args.file):
            fileLoc = args.file
        else:
            fileLoc = self.inputAnswer('File to attach to the email: ', self.validateFile)

        ## Create cronfile
        if (self.createCronFile(frequency, email, fileLoc)):
            print('Cronfile create successfully')
        else:
            print('Hmm... looks like something failed, please try again')

    """---------------------------------------------------------------------------------------
    -- FUNCTION:   inputAnswer
    -- DATE:       15/10/2016
    -- REVISIONS:  (V1.0)
    -- DESIGNER:   Anthony Smith
    -- PROGRAMMER: Anthony Smith
    -- INPUT:      prompt : string to prompt the user with
    --             validation: function point to validate the input with
    -- RETURNS:    string : the value of user input
    --
    -- NOTES:
    -- Prompts and then waits for input from the user. Validation is done through a function
    -- pointer passed in.
    --------------------------------------------------------------------------------------"""
    def inputAnswer(self, prompt, validation):
        while True:
            value = input(prompt)
            if validation(value) == True:
                return value

    """---------------------------------------------------------------------------------------
    -- FUNCTION:   validateFrequency
    -- DATE:       15/10/2016
    -- REVISIONS:  (V1.0)
    -- DESIGNER:   Anthony Smith
    -- PROGRAMMER: Anthony Smith
    -- INPUT:      frequency : string that contains the cronjob frequency
    -- RETURNS:    boolean : whether or not input is valid
    --
    -- NOTES:
    -- Validates string input to check if it's a valid cronjob frequency
    --------------------------------------------------------------------------------------"""
    def validateFrequency(self, frequency):
        entryArray = frequency.split()
        if len(entryArray) == 5:
            return True
        else:
            print('\nInvalid Frequency')
            return False

    """---------------------------------------------------------------------------------------
    -- FUNCTION:   validateEmail
    -- DATE:       15/10/2016
    -- REVISIONS:  (V1.0)
    -- DESIGNER:   Anthony Smith
    -- PROGRAMMER: Anthony Smith
    -- INPUT:      email : string that contains the recipient email
    -- RETURNS:    boolean : whether or not input is valid
    --
    -- NOTES:
    -- Validates string input to check if it's a valid email address through regex expression
    --------------------------------------------------------------------------------------"""
    def validateEmail(self, email):
        pattern = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
        if pattern.match(email):
            return True
        else:
            print('\nInvalid Email Address')
            return False

    """---------------------------------------------------------------------------------------
    -- FUNCTION:   validateFile
    -- DATE:       15/10/2016
    -- REVISIONS:  (V1.0)
    -- DESIGNER:   Anthony Smith
    -- PROGRAMMER: Anthony Smith
    -- INPUT:      fileLocation : string that contains the location of a file
    -- RETURNS:    boolean : whether or not input is valid
    --
    -- NOTES:
    -- Validates string input to check if there's an actual file at the specified location
    --------------------------------------------------------------------------------------"""
    def validateFile(self, fileLocation):
        theFile = Path(fileLocation)
        if theFile.is_file():
            return True
        else:
            print('\nInvalid File Location')
            return False

    """---------------------------------------------------------------------------------------
    -- FUNCTION:   createCronFile
    -- DATE:       15/10/2016
    -- REVISIONS:  (V1.0)
    -- DESIGNER:   Anthony Smith
    -- PROGRAMMER: Anthony Smith
    -- INPUT:      frequency : string that contains the cronjob frequency
    --             email : string that contains the recipient email
    --             fileLocation : string that contains the location of a file
    -- RETURNS:    boolean : whether or not the cronjob was created successfully
    --
    -- NOTES:
    -- Creates a temporary file that is feeded into crontab to activate the cronjob. Removes
    -- the temporary file afterwards.
    --------------------------------------------------------------------------------------"""
    def createCronFile(self, frequency, email, fileLocation):
        # generate a temporary file to store the cronjob
        template = '{} echo "Here is a requested file" | mail -s "Cron Job" -a {} {} \n'.format(frequency, fileLocation, email)
        _file = open('.temp-cron', 'w+')
        _file.write(template)
        _file.close()

        # install cronjob from temporary file
        bashCommand = 'crontab .temp-cron'
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        # remove temporary file
        os.remove('.temp-cron')

        if not error:
            return True
        else:
            return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--freq', help='How often the cronjob runs')
    parser.add_argument('--email', help='Address to send an email to')
    parser.add_argument('--file', help='Location of a file to attach to an email')
    args = parser.parse_args()

    shell = Shell(args)

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, 
        QLineEdit, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon
from enum import Enum

class ShellWindow(QWidget):

    def createTextBoxLayout(self, textBox, labelTxt):
        label = QLabel(labelTxt, self)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(textBox)
        return layout

    def __init__(self):
        super(ShellWindow, self).__init__()
        self.setWindowTitle('Cronjob')
        self.setWindowIcon(QIcon('web.png'))
        self.setGeometry(300, 300, 300, 300)

        rowLayout = QVBoxLayout()   # Keep the button on the bottom of window

        # Setup 5 textboxes
        cronCfgLayout = QHBoxLayout()
        self.minuteText = QLineEdit(self)
        cronCfgLayout.addLayout(self.createTextBoxLayout(self.minuteText, 'Minute'))

        self.hourText = QLineEdit(self)
        cronCfgLayout.addLayout(self.createTextBoxLayout(self.hourText, 'Hour'))

        self.domText = QLineEdit(self)
        cronCfgLayout.addLayout(self.createTextBoxLayout(self.domText, 'Day of Month'))

        self.monthText = QLineEdit(self)
        cronCfgLayout.addLayout(self.createTextBoxLayout(self.monthText, 'Month'))

        self.dowText = QLineEdit(self)
        cronCfgLayout.addLayout(self.createTextBoxLayout(self.dowText, 'Day of Week'))
        cronCfgLayout.addStretch()

        # Setup email address textbox
        miscCfgLayout = QVBoxLayout()
        self.emailText = QLineEdit(self)
        miscCfgLayout.addLayout(self.createTextBoxLayout(self.emailText, 'Email Address'))
        miscCfgLayout.addStretch()

        # Setup file selection box

        # Setup submit button
        submitButton = QPushButton('Create Cronjob', self)
        submitButton.move(50, 50)
        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(submitButton)

        rowLayout.addLayout(cronCfgLayout)
        rowLayout.addLayout(miscCfgLayout)
        rowLayout.addLayout(buttonLayout)
        self.setLayout(rowLayout)


class WarningResponse(Enum):
    YES = 0
    NO = 1
    ERROR = 2

class Shell:
    def __init__(self):
        ## Show warning message
        quit = ""
        while (self.validateWarning(quit)) == WarningResponse.ERROR:
            quit = input('This script creates a cronjob that could be hazardous, do you want to continue? (Y/N) ')

        if (self.validateWarning(quit) == WarningResponse.NO):
            sys.exit()

        ## Enter cronjob frequency
        frequency = ""
        while (self.validateFrequency(frequency) == False):
            frequency = input('Enter the frequency of the cronjob: ')

        ## Enter email address
        email = ""
        while (self.validateEmail(email) == False):
            email = input('Enter the recipient email: ')

        ## Enter file location
        fileLoc = ""
        while (self.validateFile(fileLoc) == False):
            fileLoc = input('Enter the file to attach to the email: ')

        ## Create cronfile
        if (self.createCronFile(frequency, email, fileLoc)):
            print('Cronfile create successfully')
        else:
            print('Hmm... looks like something failed, please try again')

    def validateWarning(self, answer):
        answer = answer.upper()
        if answer == 'Y' or answer == 'YES':
            return WarningResponse.YES
        elif answer == 'N' or answer == 'NO':
            return WarningResponse.NO
        else:
            return WarningResponse.ERROR

    def question(self, text):
        return input('text')

    def validateFrequency(self, frequency):
        if (frequency):
            return True
        else:
            return False

    def validateEmail(self, email):
        if (email):
            return True
        else:
            return False

    def validateFile(self, fileLocation):
        if (fileLocation):
            return True
        else:
            return False

    def createCronFile(self, frequency, email, fileLocation):
        template = '{} echo “Here is a requested file” | mail -s “Cron Job” -a {} {}'.format(frequency, fileLocation, email)

        _file = open('.temp-cron', 'w+')
        _file.write(template)
        _file.close()
        return True

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ShellWindow()
    window.show()
    sys.exit(app.exec_())

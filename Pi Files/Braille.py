#Importing the necessary  libraries
import shiftpi
import shiftpi_char
import RPi.GPIO as GPIO
import time
from firebase import firebase
import subprocess
from subprocess import call
import random
import urllib2
import pygame

#########################################
#From imported libraries used GPIO pins:
#shiftpi --------SER ---->25
#shiftpi --------RCLK---->24
#shiftpi --------SRCLK--->23
#shiftpi_char ---SER----->22
#shiftpi_char ---RCLK---->27
#shiftpi_char ---SRCLK--->17
#########################################

#-------------------Word Class-------------------#
#This class creates the word object for word mode.
#It has contains its constructor (depending on if we are on offline mode or not),
#next, previous, voice, random and decode functions.

class Word:

    #constructor of word class
    def __init__(self,online,words):
        #online=1 we are on online mode calling the online constructor
        if online==1:
            self.string_list= []
            if (result is None): #condition to avoid crush if the database is empty
                self.string_list= []
                self.size=len(0);
            else:
                #create our list of words from the retrieved online dictionary
                self.string_list=(words.values());
                self.size=len(self.string_list);
                self.my_string=self.string_list[0];
                #updating our file with list of words for offline mode
                file=open("words.txt","w");
                for i in range(0,self.size):
                    file.write(self.string_list[i]+"\n");
                file.close();
        else:
            #create our list of words from .txt stored file
            self.string_list=words;
            self.size=len(self.string_list);
            self.my_string=self.string_list[0];
        #print ('Displaying:', self.my_string)
    
    #change the string to a list of characters
    def get_characters(self,s):
        char_list=s;
        return char_list;
    
    #decode 4 letters to be fitted to 3 shift registers
    def serial_decode(self,l1,l2,l3,l4):
        letter1 = (l1 | l2 >> 6);
        l2=l2 & 0b111111;
        letter2 = (l2 << 2 | l3 >> 4);
        l3=l3 & 0b1111;
        letter3 = (l3 << 4 | l4 >> 2);
        return letter1,letter2,letter3;

    #set all shift registers outputs to zero
    def reset_pins(self):
        shiftpi.digitalWrite(shiftpi.ALL, shiftpi.LOW)
    
    #sets the shift register pins.
    #ref defines which pin to start setting the letter
    def shift_code(self,letter,ref):
        temp=letter;
        for i in range (7 ,-1,-1):
            if (temp & 0b1==1):
                shiftpi.digitalWrite(ref+i, shiftpi.HIGH);
            temp=temp>>1;

    #move to the next word of the list of words
    #or back to the beginning if it is the end of the list
    def next(self,i):
        self.reset_pins();
        internet_state=internetConnection();
        voiceService(internet_state,"Next")
        if (i<len(self.string_list)-1):
            #print('Moved to next word')
            i=i+1;
        else:
            #print('Moved to start of list')
            i=0;
        self.my_string=self.string_list[i];
        #print ('Displaying:', self.my_string)
        return i;

    #move to the next previous of the list of words
    #or back to the end if it is the start of the list
    def previous(self,i):
        self.reset_pins();
        internet_state=internetConnection();
        voiceService(internet_state,"Previous")
        if (i>=1):
            #print('Moved to previous word')
            i=i-1;
        else:
            #print('Moved to end of list')
            i=self.size-1;
        self.my_string = self.string_list[i];
        #print ('Displaying:', self.my_string)
        return i;
    
    #say the word the board displays using Google Voice if internet connection exist
    #or espeak in offline mode
    def voice(self):
        print ('Voice pressed')
        internet_state=internetConnection();
        voiceService(internet_state,self.my_string)

    #move to a random place in the list of words
    def randomWord(self,i):
        self.reset_pins();
        internet_state=internetConnection();
        voiceService(internet_state,"Random")
        #print ('Random pressed')
        i=random.randint(0,self.size-1)
        self.my_string=self.string_list[i];
        #print ('Displaying:', self.my_string)
        return i;

    #main function that calls all the decoding and set shift register bits functions
    def all_set(self,my_string):
        #turn to character list
        char_list = self.get_characters(my_string);
        #initialize letters
        letter1 = 0b00000000;
        letter2 = 0b00000000;
        letter3 = 0b00000000;
        letter4 = 0b00000000;
        letter5 = 0b00000000;
        letter6 = 0b00000000;
        letter7 = 0b00000000;
        letter8 = 0b00000000;
        #decode each character
        for i in range(0, len(char_list)):
            if (i == 0):
                letter1 = decode_character(char_list[0]);
            elif (i == 1):
                letter2 = decode_character(char_list[1]);
            elif (i == 2):
                letter3 = decode_character(char_list[2]);
            elif (i == 3):
                letter4 = decode_character(char_list[3]);
            elif (i == 4):
                letter5 = decode_character(char_list[4]);
            elif (i == 5):
                letter6 = decode_character(char_list[5]);
            elif (i == 6):
                letter7 = decode_character(char_list[6]);
            else:
                letter8 = self.decode_character(char_list[7]);
        #serial decode the characters in pair of 4s
        new_letter1, new_letter2, new_letter3 = self.serial_decode(letter1, letter2, letter3, letter4);
        new_letter4, new_letter5, new_letter6 = self.serial_decode(letter5, letter6, letter7, letter8);
        #reset register pins
        #self.reset_pins();
        #set register pins
        self.shift_code(new_letter1, 0);
        self.shift_code(new_letter2, 8);
        self.shift_code(new_letter3, 16);
        self.shift_code(new_letter4, 24);
        self.shift_code(new_letter5, 32);
        self.shift_code(new_letter6, 44);

#-------------------Letter Class-------------------#
#This class creates the word object for word mode.
#It has contains its constructor (depending on if we are on offline mode or not),
#next, previous, voice, random and decode functions.

class Letter:
    
    #constructor of word class
    def __init__(self):
        self.string_list=self.characterList();
        self.size=len(self.string_list);
        self.my_string=self.string_list[0];
        #print ('Displaying:', self.my_string)
    
    #create the list of all letters
    def characterList (self):
        list=[]
        list.append('a');
        list.append('b');
        list.append('c');
        list.append('d');
        list.append('e');
        list.append('f');
        list.append('g');
        list.append('h');
        list.append('i');
        list.append('j');
        list.append('k');
        list.append('l');
        list.append('m');
        list.append('n');
        list.append('o');
        list.append('p');
        list.append('q');
        list.append('r');
        list.append('s');
        list.append('t');
        list.append('u');
        list.append('v');
        list.append('w');
        list.append('x');
        list.append('y');
        list.append('z');
        return list;

    #sets the shift register pins.
    #ref defines which pin to start setting the letter
    def shift_code(self,letter,ref):
        temp=letter;
        for i in range (7 ,-1,-1):
            if (temp & 0b1==1):
                shiftpi_char.digitalWrite(ref+i, shiftpi_char.HIGH);
            temp=temp>>1;

    #set all shift registers outputs to zero
    def reset_pins(self):
        shiftpi_char.digitalWrite(shiftpi_char.ALL, shiftpi_char.LOW)
    
    #main function that calls all the decoding and set shift register bits functions
    def all_set(self,my_string):
        #self.reset_pins();
        letter=decode_character(my_string);
        self.shift_code(letter, 0);
    
    #move to the next letter of the list of letters
    #or back to the beginning if it is the end of the list
    def next(self,i):
        self.reset_pins();
        internet_state=internetConnection();
        voiceService(internet_state,"Next")
        if (i<len(self.string_list)-1):
            #print('Moved to next letter')
            i=i+1;
        else:
            #print('Moved to start of list')
            i=0;
        self.my_string=self.string_list[i];
        #print ('Displaying:', self.my_string)
        return i;
    
    #move to the previous letter of the list of letters
    #or back to the end if it is the start of the list
    def previous(self,i):
        self.reset_pins();
        internet_state=internetConnection();
        voiceService(internet_state,"Previous")
        if (i>=1):
            #print('Moved to previous letter')
            i=i-1;
        else:
            #print('Moved to end of list')
            i=self.size-1;
        self.my_string = self.string_list[i];
        #print ('Displaying:', self.my_string)
        return i;
    
    #say the letter the board displays using Google Voice if internet connection exist
    #or espeak in offline mode
    def voice(self):
        #print ('Voice pressed')
        internet_state=internetConnection();
        voiceService(internet_state,self.my_string);

    #move to a random place in the list of letters
    def randomLetter(self,i):
        self.reset_pins();
        internet_state=internetConnection();
        voiceService(internet_state,"Random")
        #print ('Random Letter pressed')
        i=random.randint(0,self.size-1)
        self.my_string=self.string_list[i];
        #print ('Displaying:', self.my_string)
        return i;

#-------------------Global Functions-------------------#

#This function turns the character to the braille equivalent
#1 is for dot, 0 for blank
#the last 00 exist always since the output will be fed up to a
#8 bit shift register
def decode_character(c):
    ref=97; #97 ASCII for a
    if (ord(c)==ref):
        a=0b10000000;
    elif (ord(c)==ref+1):
        a = 0b10100000;
    elif (ord(c)==ref+2):
        a = 0b11000000;
    elif (ord(c)==ref+3):
        a = 0b11010000;
    elif (ord(c)==ref+4):
        a = 0b10010000;
    elif (ord(c)==ref+5):
        a = 0b11100000;
    elif (ord(c)==ref+6):
        a = 0b11110000;
    elif (ord(c)==ref+7):
        a = 0b10110000;
    elif (ord(c)==ref+8):
        a = 0b01100000;
    elif (ord(c)==ref+9):
        a = 0b01110000;
    elif (ord(c)==ref+10):
        a = 0b10001000;
    elif (ord(c)==ref+11):
        a = 0b10101000;
    elif (ord(c)==ref+12):
        a = 0b11001000;
    elif (ord(c)==ref+13):
        a = 0b11011000;
    elif (ord(c)==ref+14):
        a = 0b10011000;
    elif (ord(c)==ref+15):
        a = 0b11101000;
    elif (ord(c)==ref+16):
        a = 0b11111000;
    elif (ord(c)==ref+17):
        a = 0b10111000;
    elif (ord(c)==ref+18):
        a = 0b01101000;
    elif(ord(c)==ref+19):
        a = 0b01111000;
    elif(ord(c)==ref+20):
        a = 0b10001100;
    elif (ord(c)==ref+21):
        a = 0b10101100;
    elif (ord(c)==ref+22):
        a = 0b01110100;
    elif (ord(c)==ref+23):
        a = 0b11001100;
    elif (ord(c)==ref+24):
        a = 0b11011100;
    elif (ord(c)==ref+25):
        a = 0b10011100;
    return a;

#This function checks for internet connection
#1=successfull internet connection
def internetConnection():
    try:
        urllib2.urlopen("http://www.google.com").close();
    except urllib2.URLError as err:
        #print "No Internet Connection"
        state=0;
    else:
        #print "Internet Connection"
        state=1;
    return state;

#This functions uses Google assistant is state=1 (Internet)
#else espeak to say the input string
def voiceService(state,input):
    if state==1:
        subprocess.call(['./speech.sh',input]);
    else:
        call([cmd_beg+cmd_out+input+cmd_end], shell=True);
        pygame.mixer.init()
        pygame.mixer.music.load("Text.wav")
        pygame.mixer.music.play()

if __name__ == '__main__':
    #print('Rasberry pi started.');

    #GPIO, registers and espeak initial configuration
    #print('Configuring registers, buttons, espeak setting and GPIO configuration')
    cmd_beg='espeak -ven+f3 -k5 -s150 '
    cmd_end=' | aplay /home/pi/Text.wav 2>/dev/null'
    cmd_out='--stdout > /home/pi/Text.wav '
    shiftpi.shiftRegisters(6);
    shiftpi_char.shiftRegisters(1); 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)                        #Next Button to GPIO26
    GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)                        #Previous Button to GPIO13
    GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)                        #Voice Button to GPIO16
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)                         #Random Button to GPIO6
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)                         #Refresh Button to GPIO5
    GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)                        #Change Button to GPIO12
    #GPIO.setup(4,GPIO.OUT); #LED LIght
    #print('Registers and button configured successfully')
    #GPIO.output(4,GPIO.HIGH);
    #Intitial board configuration. Checks for connection.
    #If connection exists sets word mode from firebase
    #else gets to letter mode.
    internet_state=internetConnection();
    if (internet_state==1):
        #GPIO.output(4,GPIO.HIGH);
        #print('Connecting to firebase...');
        i=0;
        state=1; #1 state for word mode
        firebase = firebase.FirebaseApplication('https://brailler-7dc17.firebaseio.com/', None)
        result = firebase.get('/Boards/1/words', None)
        if (result is None):
            #print ('Connection failed');
            subprocess.call(['./speech.sh',"Refresh Failed"]);
        else:
            #print('Firebase connected results we retrieved:...')
            #print(result)
            #print('Preparing Braille word library')
            my_word=Word(1,result);
            #print('Braille successfully configured')
    else:
        #print "No Internet Connection"
        #GPIO.output(4,GPIO.LOW);
        i=0;
        state=0; #0 state for letter mode
        my_letter=Letter();
    voiceService(internet_state,"Hi, I am Braillio");
    previous_internet=internet_state;
    
    #Main loop
    while True:
            #In each iteration get the button state.
            next_button_state = GPIO.input(26);
            previous_button_state = GPIO.input(13);
            voice_state = GPIO.input(16);
            random_state = GPIO.input(6);
            refresh_state = GPIO.input(5);
            change_state = GPIO.input(12);
            
            #Change modes between letter and word
            if change_state==False:
                if state==1:
                    internet_state=internetConnection();
                    voiceService(internet_state,"Change to letter mode")
                    state=0;
                    i=0;
                    my_word.reset_pins(); #reset pins
                    del my_word; #delete our word object
                    my_letter=Letter();
                else:
                    internet_state=internetConnection();
                    voiceService(internet_state,"Change to word mode")
                    state=1;
                    i=0;
                    my_letter.reset_pins(); #reset pins
                    with open("words.txt","r") as myfile:
                        lines=myfile.read().splitlines();
                    my_word=Word(0,lines);
                    del my_letter; #delete our letter object
                time.sleep(1);     

            #Refresh our .txt file for word mode
            if refresh_state==False:
                internet_state=internetConnection();
                if internet_state==1:
                    voiceService(internet_state,"Successful Refresh");
                    result = firebase.get('/Boards/1/words', None)
                    if (result is None):
                        #print ('Connection failed');
                        subprocess.call(['./speech.sh',"Refresh Failed"]);
                    else:
                        #print('Firebase connected results we retrieved:...')
                        #print(result)
                        #print('Preparing Braille word library')
                        my_word=Word(1,result);
                        #print('Braille successfully configured')
                else:
                    voiceService(internet_state,"RefreshFailed");

            #Next button
            if next_button_state==False:
                if state==1:
                    i=my_word.next(i);
                else:
                    i=my_letter.next(i);
                time.sleep(1);

            #Previous button
            if previous_button_state==False:
                if state==1:
                    i=my_word.previous(i);
                else:
                    i=my_letter.previous(i);
                time.sleep(1);

            #Voice button
            if voice_state==False:
                if state==1:
                    my_word.voice();
                else:
                    my_letter.voice();
                time.sleep(1);

            #Random button
            if random_state==False:
                if state==1:
                    i=my_word.randomWord(i);
                else:
                    i=my_letter.randomLetter(i);
                time.sleep(1);

            #State decided which object to set
            if state==1:
                my_word.all_set(my_word.my_string);
            else:
                my_letter.all_set(my_letter.my_string);
            
            
        
        







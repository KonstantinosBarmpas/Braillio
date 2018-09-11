import RPi.GPIO as GPIO
import time
import urllib2


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

if __name__ == '__main__':
    
    GPIO.setmode(GPIO.BCM);
    GPIO.setup(4,GPIO.OUT); #LED LIght
    while True:
        
        internet_state=internetConnection();
        if (internet_state==1):
            print("yes");
            GPIO.output(4,GPIO.HIGH);
        else:
            print("no");
            GPIO.output(4,GPIO.LOW);
        time.sleep(3);
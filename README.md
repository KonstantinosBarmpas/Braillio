# **Braillio - 2nd Year Project**

## 2nd year project at Imperial College London department of Electrical and Electronic Engineering (2018).

---

[//]: # (Images)

[image1]: ./images/Image1.jpg "Image 1"
[image2]: ./images/Image2.jpg "Image 2"
[image3]: ./images/Image3.jpg "Image 3"
[image4]: ./images/Image4.jpg "Image 4"
[image5]: ./images/Image5.jpg "Image 5"
[image6]: ./images/Image6.jpg "Image 6"
[image7]: ./images/Image7.jpg "Image 7"

**Braillio - 2nd Year Project**

![image1]
![image2]

Goal of the project:

The  development  and  design  of  an  electronic  Braille  device  intended  to  aid  in  the education of young visually-impaired children.  The board includes a refreshable electronic Braille display consisting of one large letter followed by four smaller letters, an additional functionality that allows wordsto be added to the database and a speech feature that vocalise’s letters, words and button functions.  The board must be portable, easy to use and cost effective. Different concept generation and selection techniques were discussed showing the team’s thought pro-cesses.  Method matrices are a primary example of some of the techniques used throughout the initial design. There were complications during the process, however working as a team, solutions were created to overcomesuch hurdles.  The project required special planning, therefore management roles and technical parts of therover were allocated to different members in order to split up the work efficiently. Development  goals  were  split  into  subsections  consisting  of  hardware,  digital  hardware  and  softwaredesign.  Thorough research of linear actuators, multiplexing outputs, central processing and power circuitrywas made followed by intricate design and implementation.  Finally, the mechanical design of the board wasrealised and the industrial design, ergonomics and manufacturing conditions reviewed.

Raspberry pi:

The board has two modes ”Letter mode” and ”Word mode” while it also comes with an online and an offline version.  For each mode a different object (Word class and Letter class) is created and used.  If the user changes modes, the previous object is deleted and an object of the new mode is created.  Each object has two important member variables self.stringlist and self.mystring.  The first one contains all the possible letters / words thatthe user can display while the latter determines the letter / word that is being displayed on the board.  When the Raspberry pi powers up the Braille.py file runs and configures the board depending on the internet connectivity.  The Braille.py file consists of two classes (Word and Letter), one main function and three global functions as they are described below.

![image3]

If  the  board  has  established  an  Internet  connection  the  board  connects  to  its  branch  of  the  Firebase  on-line  database  and  the  Word  class  constructor  is  called.   This  creates  a  word  object  with  member  variableself.stringlist, a list of all the retrieved words from the database, and sets the self.mystring to the first elementof that list.  In addition, all the words are saved in a .txt file which is used in the offline word mode in the Wordclass constructor to create the self.stringlist variable.  If no Internet connection exists,  the board switches to Letter mode which creates a letter object with all alphabet letters in self.stringlist and self.mystring the letter ’a’.After the board has been configured, the variable state indicates the mode of the board (1 for word and 0 forletter) and an infinite while loop runs which checks if any of the board’s six buttons has been pushed down in order to call the corresponding member function of the currently used object as they are indicated in the table and  their  functionalities. The  exception  is  the  ”refresh  button”  which  calls  theconstructor of the Word class to update the self.stringlist member list and the .txt, if internet connection exists,and ”change mode button” which deletes the previous object and creates the new object giving the previous state. Every time a button is pressed the board speaks the name of the button that has been pressed and performsits functionality. In the end of each loop iteration the allset() member function is called that sets the displayed word / letter based on the object’s self.mystring member variable. The encoding process is the translation of each letter to a series of bits that will set the corresponding pins ofthe shift register to HIGH or LOW. While for Letter mode a simple call of the global decodeCharacter(char c) is enough, Word mode requires multiplexing the output series of bits.  Each Braille letter requires 6 pins while the used shift registers have 8 output.  Our approach is the use of the last unused pins (always set to zero afterdecodeChar function) for the next letter. In that way it is possible for 3 shift registers to be used to encode 4 letters. That involves first call of the decodeCharacter function for each character and then to perform logicalshifts in order to generate the output series of bits.

![image4]

![image5]

Android app:

A supplementary Android app has been developed to enable users to connect to their board’s database and set new words or remove old ones.  The app requires the board number and the password which the users can changeby clicking on the ”CHANGE PASSWORD” button.  Once successfully logged into their board’s database, a listof all the board’s words will appear.  They can add new words by typing them and clicking ”ADD WORD” orthey can remove existed words by just clicking on the word.  Finally, the users can set up their boards Wi-Fi byenabling their Bluetooth services, clicking on the ”SET UP WIFI” button and typing their SSID and password. The database is configured to ”no authentication” to read data and to ”package and password authentication” to write data on each branch meaning that only the users can write to the database only through the app andwith the right combination of board number and password.

![image6]

The implementation of the Word mode on our board has been a big challenge. Hard coding the words wasthe original approach but it was decided that the users need to be able to add new words.  We tackled thisobstacle  with  Firebase  online  database  and  the  supplementary  Android  app.   But  this  approach  requires  anInternet connection.  In order to overcome this issue, we used the Bluetooth functionality of the Raspberry pizero simply by using the Android app to send the SSID and password of the network to the pi board seriallyusing Bluetooth. When the Raspberry pi powers up except of the Braille.py file runs also the bluetooth-RPi-wifi.py which checks for Bluetooth connection.  Once successfully received data, it configuresthe board’s Wi-Fi settings accordingly. Finally, the internetLED.py file also runs along withthe other two .py files. This file turns on a LED on the board to notify the user that the board is connected to the internet.

![image7]

---



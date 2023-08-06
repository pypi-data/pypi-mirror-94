from dt_structures3x.hashtable import Node, Hashtable
import time
from termcolor import cprint
import os.path

class Checker:
    NULL_CHAR = [".", 
    ",", 
    "!", 
    ";", 
    ":", 
    "?", 
    "%", 
    "~", 
    "+", 
    "=", 
    "-", 
    "_",
    "*",
    "@",
    "#",
    "&",
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    ]
    def __init__(self, text:str, languageinp:str):
        """
        Available languages are:\n
        english\n
        german\n
        french\n
        spanish\n
        italian\n

        Please choose one of them and type in exactly what's shown above!
        """
        self.text = text
        self.ht = None
        self.language = languageinp.lower()
        self.clean()
        
    def bucketize(self):
        """
        Not something you are going to use!
        Returns true if success, for more information on Hashtables, visit: https://https://harvard90873.readthedocs.io/en/latest/Python%20Data%20Structures%203x.html
        """
        if not self.check_lang(self.language):
            cprint("Invalid language!", "red")
            return False
        self.clean()
        buffer = self.text
        words = buffer.split()
        ht = Hashtable()
        current_directory = os.path.dirname(__file__)
        determined_dict = os.path.join(current_directory, f'{self.language}.txt')
        with open(determined_dict, "r") as dic:
            words = dic.readlines()
            for i in words:
                ht.insert(Node(i))
        self.ht = ht
        return True
    
    def check(self):
        if not self.check_lang(self.language):
            cprint("Invalid language!", "red")
            return 
        self.clean()
        self.bucketize()
        buffer = self.text
        words = buffer.split()
        n = 0
        current_directory = os.path.dirname(__file__)
        determined_dict = os.path.join(current_directory, f'{self.language}.txt')
        with open(determined_dict, "r") as some:
            n = len(some.readlines())
        statistics = {
            "total_words": len(words),
            "misspelled_words": [],
            "words_in_dictionary": n
        }
        
        start_time = time.time()
        wrong = 0
        for word in words:
            if self.ht.lookup(Node(word.lower())) == False:
                # Meaning if the word does not exist
                wrong += 1
                statistics["misspelled_words"].append(word)
        # Collect statistics
        statistics["runtime"] = time.time() - start_time
        statistics["misspelled_num"] = wrong
        statistics["token"] = "47874587235697124309"
        self.visualize(statistics)
        return statistics

    def clean(self):
        """
        Not something you are going to use!
        ...Cleans any non-alphabet chars
        """
        if not self.check_lang(self.language):
            cprint("Invalid language!", "red")
            return False
        if self.text == None:
            return False
        buffer = self.text
        for i in buffer:
            if i in self.NULL_CHAR:
                indexToRemove = buffer.index(i)
                buffer = buffer[0 : indexToRemove : ] + " " + buffer[indexToRemove + 1 : :]
        self.text = buffer
        
        return True

    def visualize(self, statistics:dict):
        """
        Don't call this method! It would be called for you at some point!
        """
        if not self.check_lang(self.language):
            cprint("Invalid language!", "red")
            return
        if not statistics["token"] or statistics["token"] != "47874587235697124309":
            cprint("Don't call this method! It would be called for you at some point!", "yellow")
            return

        total = statistics["total_words"]
        wrong_num = statistics["misspelled_num"]
        dict_num = statistics["words_in_dictionary"]
        wrong = statistics["misspelled_words"]
        rt = statistics["runtime"]
        res = f"Total words: {total}\nNumber of misspelled words: {wrong_num}\nNumber of words in dictionary: {dict_num}\nMisspelled words: {wrong}\nLookup time(s): {rt}"
        cprint(res, "green")
        return res
        

    def check_lang(self, lang):
        supported_langs = ["english",
        "german",
        "french",
        "spanish",
        "italian"]
        if lang not in supported_langs:
            return False
        return True

import json
from typing import Dict
from pprint import pprint
import sqlite3
from collections import Counter
from collections import defaultdict
import re


class MessageBoardAPIWrapper:
    """
    Wrapper around the messageboard API

    http://localhost:8080/api/
    """
    #from django.db.backends.sqlite3 import connection

    

    def __init__(self):
        
        # DATABASE CONNECTION
        self.con = sqlite3.connect("src/db.sqlite3")
        self.cursor = self.con.cursor()


    def num_messages(self) -> int:
        """
        Returns the total number of messages.
        """
        
        self.cursor.execute("SELECT id FROM messageboard_message")
        res1 = len(self.cursor.fetchall())   
        return res1

    def most_common_word(self) -> str:
        """
        Returns the most frequently used word in messages.
        """
        # This script returns most recurring word in whole message of cursor.fetchall() 
        # not checking each message for most used word and compareng them for another line. 
        x=self.num_messages()
        
        self.cursor.execute("SELECT content FROM messageboard_message")
        data = str(self.cursor.fetchall())
        data1 = re.sub(r'[^\w\s]', '', data)
        datalower = data1.lower() 
        datalist = datalower.split(" ")    
        # most = max(datalist)
        temp=defaultdict(int)  
            
        # create count dictionary from list of words
        for sub in datalist:
            temp[sub] += 1
        
        # getting max frequency
        res2 = max(temp, key=temp.get)
        # print(result)
        #print(temp)
        # print("Word with maximum frequency : " + str(res))
        return res2
           
            
            
        
        
        


    def avg_num_words_per_sentence(self) -> float:
        """
        Returns the average number of words per sentence.
        """
        
        self.cursor.execute("SELECT content FROM messageboard_message")
        res1 = len(self.cursor.fetchall())  
        data = str(self.cursor.fetchall())
        data1 = re.sub(r'[^\w\s]', '', data)
        datalower = data1.lower() 
        datalist = datalower.split(" ")    

        res3 = len(datalist) / res1

        return float(res3)
           
    

    def avg_num_msg_thread_topic(self) -> Dict[str, float]:
        """
        Returns the average number of messages per thread, per topic.
        
        """

        self.cursor.execute("SELECT content FROM messageboard_message")
        messagesqty = len(self.cursor.fetchall())  

        self.cursor.execute("SELECT title FROM messageboard_thread")
        threadsqty = len(self.cursor.fetchall())  
        
        self.cursor.execute("SELECT title FROM messageboard_topic")
        topicsqty = len(self.cursor.fetchall())
        my_dict = {str(messagesqty / threadsqty): float(messagesqty / topicsqty)}
        return my_dict

    def _as_dict(self) -> dict:
        """
        Returns the entire messageboard as a nested dictionary.
        """
        
        self.cursor.execute("SELECT * FROM messageboard_message")
        messages = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM messageboard_thread")
        threads = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM messageboard_topic")
        topics = self.cursor.fetchall()
        
        final=dict()
        all_messages =dict()
        all_topics =dict()
        all_threads =dict()
        
        for topic in topics:       
            for thread in threads:
                if topic[0] == thread[4]:
                    for message in messages:
                        if thread[0] == message[4]:
                            all_threads[thread]=message
                            all_topics[topic]=all_threads

            
         
        return str(all_topics) 
               
    def to_json(self) -> None:
        """
        Dumps the entire messageboard to a JSON file.
        """
        with open("messageboard.json", "w") as f:
            f.write(json.dumps(self._as_dict(), indent=4))



def main():
    """
    Returns information about the messageboard application
    """



    messageboard = MessageBoardAPIWrapper()

    print(f"Total number of messages: {messageboard.num_messages()}")
    print(f"Most common word: {messageboard.most_common_word()}")
    print(
        f"Avg. number of words per sentence:"
        f"{messageboard.avg_num_words_per_sentence()}"
    )
    print(
        f"Avg. number of messages per thread, per topic:"
        f"{messageboard.avg_num_msg_thread_topic()}"
    )

    messageboard.to_json()
    print("Message Board written to `messageboard.json`")
    print({messageboard._as_dict()})
    
    return
    


if __name__ == "__main__":
    main()

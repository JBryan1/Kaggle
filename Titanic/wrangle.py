import numpy as np
import pandas as pd
import re as re
import math as math

def wrangle(df):
    """For Titanic data. Creates new dummy features for cabin letter, embarked departure locations, ticket prefix presence, and available ticket prefix and numbers"""
    def uniqueLetters(cabin):
        '''Input list of unique Cabin numbers and output unique letters from entire list'''
        uniq_letters = set()
        for e in cabin:
            if type(e) is not str:
                next
            else:
                f = list(set(e))
                f = list(filter(lambda i: not str.isdigit(i), f))
                uniq_letters.update(f)
        uniq_letters.discard(" ") 
        return uniq_letters
    
    ###Separate Prefix and Numbers from Ticket
    df["Ticket"] = df['Ticket'].str.replace('[^\w\s]','') #Replace punctuation with empty string
    df["Ticket_Num"] = np.nan #Create new column for ticket numbers with NaN value
    df["Ticket_Prefix"] = "" #Create new colum for ticket prefix letters with empty string

    for index, row in df.iterrows(): #iterate over each row of titanic training data
        list_string = row["Ticket"].split() #split Ticket value into list of strings
        n = len(list_string) #store length of list
        if n == 1 and list_string[0].isdigit(): #store new ticket number value as integer of current value from list if there is only 1 string element and is numeric
            df.loc[index ,"Ticket_Num"] = int(list_string[0])

        elif n == 1: #store new ticket prefix value if there is only 1 element in list and it is not numeric
            df.loc[index ,"Ticket_Prefix"] = list_string[0]

        else: #store new ticket prefix and number values 
            df.loc[index ,"Ticket_Prefix"] = " ".join(list_string[0:n-1])
            df.loc[index ,"Ticket_Num"] = int(list_string[n-1])
    df = df.drop('Ticket', 1) #drop Ticket column
    
    ### Create Binary Column for Cabin
    df["Cabin_Yes"] = 0
    for index, row in df.iterrows():
        if type(row["Cabin"]) != float:
            df.loc[index,'Cabin_Yes'] = 1
    
    ### Create Columns for Unique Cabin Letters 
    cabin = list(df.Cabin.unique())
    uniqueLetters = uniqueLetters(cabin) #Retrieve unique cabin letters
    print(uniqueLetters)
    #Create numeric binary columns for each letter
    for letter in uniqueLetters:
        df["Cabin_" + letter] = 0

    #Fill data for each column letter
    for letter in uniqueLetters: #Iterate over each unqiue letter from Cabin number in data
        for index, row in df.iterrows(): #Iterate over each row of data
            if type(row["Cabin"]) != float: #Continue if Cabin value is not floating, which would mean not NaN
                if row["Cabin"].find(letter) != -1: #Look to see if unique letter is in Cabin value for row
                    df.loc[index,"Cabin_" + letter] = 1 #Assign 1 if unique Cabin letter is found

    df = df.drop('Cabin', 1) #drop Cabin column
    
    ### Drop PassengerID and Name
    df = df.drop(["PassengerId","Name"], 1)
    
    ### Add Dummy Variables for Sex, Embarked, and Ticket_Prefix
    df = df.join(pd.get_dummies(df["Sex"]))
    df = df.join(pd.get_dummies(df["Embarked"], prefix="Embarked"))
    df = df.join(pd.get_dummies(df["Ticket_Prefix"], prefix="Ticket_Prefix"))
    df = df.drop(["Sex","Embarked","Ticket_Prefix"], 1)
    
    return df

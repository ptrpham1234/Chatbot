#!/usr/bin/env python3
#############################################################################################################
# Assignment:          Homework 1
# Author:              Peter Pham (pxp180041)
# Course:              CS 4348.002
# Date Started:        03/20/2022
# IDE:                 pycharm
#
# Description:
#
#############################################################################################################

################# I M P O R T S #################
import re
import aiml
import os
import logging
import nltk
from Person import Person
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer

stopwords = set(stopwords.words('english'))

# setup the save directory
basePath = r"".join(os.getcwd())  # get the current directory
dataPath = r"".join(os.path.join(basePath, 'data'))


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def main():

    BRAIN_FILE = os.path.join(basePath, "bot_brain.brn")

    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)
    chatLog = os.path.join(basePath, "chat.log")

    kernel = aiml.Kernel()

    # so it doesn't keep on saying loading
    # kernel.verbose(isVerbose=False)

    if os.path.exists(BRAIN_FILE):
        print("Loading from brain file: " + BRAIN_FILE)
        kernel.loadBrain(BRAIN_FILE)
    else:
        print("Parsing aiml files")

        kernel.learn("startup.xml")
        kernel.respond("LEARN AIML")

        print("Saving brain file: " + BRAIN_FILE)
        # kernel.saveBrain(BRAIN_FILE)

    intro()

    pronoun = ""

    with open(chatLog, 'w') as log:
        while True:
            message = input("user> ").lower()

            log.write("user> " + message + r"\n")

            if message == "quit":
                username = kernel.getPredicate("username")
                print("Bot> Goodbye " + username)
                exit()

            elif message == "save":
                kernel.saveBrain("bot_brain.brn")

            else:
                message, pronoun = processMessage(message, pronoun)
                bot_response = kernel.respond(message)
                print("Bot> " + bot_response)
                log.write("Bot> " + bot_response + r"\n")


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def intro():
    print("Bot> Hi my name is Karl. I'm a bird bot.")
    print("Bot> Here are the list of bird species I know:")
    print("Northern Cardinal            American Goldfinch")
    print("Northern Mockingbird         House Finch")
    print("Mourning Dove                Carolina Chickadee")
    print("White-winged Dove            Carolina Wren")
    print("Great-tailed Grackle         Blue Jay")
    print("Yellow-rumped Warbler        Barn Swallow")
    print("House Sparrow                Eastern Phoebe")
    print("Ruby-crowned Kinglet")
    print("\nBot> You can ask me about their diet, size and lifespan")
    print("Bot> I can also give you a random fact about a bird")
    print("Bot> I also know a couple of jokes if you're into that.")
    print("Bot> Lets start with your name. What is your name?")


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def processMessage(message, pronoun):

    tokens = tokenize(message)
    new_tokens = list(tokens)
    pos_tags = pos(new_tokens)
    return_message = ""
    newPronoun = False

    size_words = {"size", "big", "large", "width", "dimensions", "long"}
    life_words = {"live"}
    food_words = {"eat", "food", "diet"}

    for word in new_tokens:
        if word in stopwords:
            new_tokens.remove(word)

    with open(os.path.join(dataPath, 'birdnames.set'), 'r') as file:
        bird_names = file.read().lower().replace("-", " ")
        bird_names = set(tokenize(bird_names))

        for word in new_tokens:
            if word in bird_names:
                return_message += word + " "
                newPronoun = True

        if newPronoun:
            pronoun = return_message

        for pairing in pos_tags:
            if pairing[1] == "PRP":
                return_message = pronoun

    for pairing in pos_tags:
        # print(pairing[1])
        if pairing[0] in food_words:
            return_message = "food " + return_message
        elif pairing[0] in life_words:
            return_message = "life " + return_message
        elif pairing[0] in size_words:
            return_message = "size " + return_message

    if return_message == "":
        return_message = TreebankWordDetokenizer().detokenize(tokens)

    return return_message, pronoun


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def tokenize(string):
    string = string.replace("\'", "")
    return nltk.word_tokenize(string)

#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def pos(tokens):
    return nltk.pos_tag(tokens)



#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        02/08/2022
#  *
#  * Description:
#  * Main purpose is to check for arguments and start main function
#  *
#  * Parameters:
#############################################################################################################
if __name__ == '__main__':
    main()
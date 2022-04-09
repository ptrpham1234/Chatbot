#!/usr/bin/env python3
#############################################################################################################
# Assignment:          Homework 1
# Author:              Peter Pham (pxp180041)
# Course:              CS 4348.002
# Date Started:        04/01/2022
# IDE:                 pycharm
#
# Description:
#
#############################################################################################################

################# I M P O R T S #################
import re
import os
import aiml
import nltk
import pickle
from Person import Person
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize.treebank import TreebankWordDetokenizer

# Init the Wordnet Lemmatizer
lemmatizer = WordNetLemmatizer()

stopwords = set(stopwords.words('english'))

# setup the save directory
basePath = r"".join(os.getcwd())  # get the current directory
dataPath = r"".join(os.path.join(basePath, 'data'))

# initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/01/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def main():
    BRAIN_FILE = os.path.join(basePath, "bot_brain.brn")
    chatLog = os.path.join(basePath, "chat.log")
    userFile = os.path.join(basePath, "user.pickle")

    notExit = True

    kernel = aiml.Kernel()

    likes = list()
    dislikes = list()
    sessionId = 1234

    # so it doesn't keep on saying loading
    # kernel.verbose(isVerbose=False)

    # see if a brain file exists, if it does then load it in
    if os.path.exists(BRAIN_FILE):
        print("Loading from brain file: " + BRAIN_FILE)
        kernel.loadBrain(BRAIN_FILE)
    # if not then load in the aiml files
    else:
        print("Parsing aiml files")

        kernel.learn("startup.xml")
        kernel.respond("LEARN AIML")

        print("Saving brain file: " + BRAIN_FILE)
        kernel.saveBrain(BRAIN_FILE)

    # if a user data file exists the load it in
    if os.path.exists(userFile):
        with open(userFile, "rb") as file:
            user = pickle.load(file)

            # get user's name
            if user.getName() is not None:
                print(user.getName())
                kernel.setPredicate("username", user.getName())
            # get the user's age
            if user.getAge() is not None:
                kernel.setPredicate("age", user.getAge())
            # get the user's likes and dislikes
            likes = user.getLikes()
            dislikes = user.getDislikes()

    # print the intro
    intro()

    # declare the pronoun var. holds the noun of the previously mentioned bird
    pronoun = ""

    # start a chat log
    with open(chatLog, 'w') as log:
        # keep on asking the user until the quit keyword is mentioned
        while notExit:
            # asks the user
            message = input("user> ").lower()

            # log it
            log.write("user> " + message + r"\n")

            # if the user enters a quit
            if message == "quit":
                # open the user file to write
                with open(userFile, "wb") as file:
                    # get the user data from the bot
                    username = kernel.getPredicate("username")
                    age = kernel.getPredicate("age")

                    # create a user class to save
                    user = Person(name=username, age=age, likes=likes, dislikes=dislikes)

                    # dump it to the pickle file
                    pickle.dump(user, file)

                    # Karl says goodbye
                    print("Karl> User file saved")
                    print(kernel.respond(message))
                    notExit = False

            elif message == "save":
                kernel.saveBrain("bot_brain.brn")

            # process the message
            else:
                message, pronoun, newLikes, newDislikes = processMessage(message, pronoun, likes, dislikes)

                # send the processed messaged to Karl
                bot_response = kernel.respond(message)
                print("Karl> " + bot_response + "\n")
                log.write("Karl> " + bot_response + r"\n")


#############################################################################################################
#  * Function:            intro
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/01/2022
#  *
#  * Description:
#  * Dialogue for the intro of the bot. Greats the user and tells them what he does.
#############################################################################################################
def intro():
    print("\n\nKarl> Hi my name is Karl. I'm a bird bot.")
    print("Karl> Here are the list of bird species I know:")
    print("     Northern Cardinal            American Goldfinch")
    print("     Northern Mockingbird         House Finch")
    print("     Mourning Dove                Carolina Chickadee")
    print("     White-winged Dove            Carolina Wren")
    print("     Great-tailed Grackle         Blue Jay")
    print("     Yellow-rumped Warbler        Barn Swallow")
    print("     House Sparrow                Eastern Phoebe")
    print("     Ruby-crowned Kinglet")
    print("\nKarl> You can ask me about their diet, size and lifespan")
    print("Karl> I can also give you a random fact about a bird")
    print("Karl> I also know a couple of jokes if you're into that.")
    print("Karl> Type \"quit\" anytime to close me")
    print("Karl> Lets start with you. Tell me about yourself like your name, age, and/or likes and dislikes.")


#############################################################################################################
#  * Function:            functionality
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/01/2022
#  *
#  * Description:
#  * Tells the user what the functionality is of the bot
#############################################################################################################
def functionality():
    print("\n\nKarl> Here are the list of bird species I know:")
    print("     Northern Cardinal            American Goldfinch")
    print("     Northern Mockingbird         House Finch")
    print("     Mourning Dove                Carolina Chickadee")
    print("     White-winged Dove            Carolina Wren")
    print("     Great-tailed Grackle         Blue Jay")
    print("     Yellow-rumped Warbler        Barn Swallow")
    print("     House Sparrow                Eastern Phoebe")
    print("     Ruby-crowned Kinglet")
    print("\nKarl> You can ask me about their diet, size and lifespan or a general fact")
    print("Karl> I can also give you a random fact about any bird. Just ask for a random bird fact!")
    print("Karl> I also know a couple of jokes if you're into that.")
    print("Karl> Type \"quit\" anytime to close me")


#############################################################################################################
#  * Function:            processMessage
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/01/2022
#  *
#  * Description:
#  * Process the message from the user. It can be a like or dislike statement, a bird question or everything
#  * else.
#############################################################################################################
def processMessage(message, pronoun, likes, dislikes):
    message = removePunctuation(message)
    tokens = tokenize(message)
    tokens = token_lemmatize(tokens)
    new_tokens = list(tokens)
    pos_tags = pos(new_tokens)
    return_message = ""
    newPronoun = False
    skip = False
    find = False

    # if the message is empty return the empty message command to Karl
    if message == "":
        return "EMPTY MESSAGE", pronoun, likes, dislikes

    # set of topics about a word to match and look for
    size_words = {"size", "big", "large", "width", "dimensions", "long"}
    life_words = {"live", "reside", "inhabit", "occupy", "located", "locate"}
    food_words = {"eat", "food", "diet"}
    about_words = {"about", "facts", "fact"}

    # if the user asks what the bot can do
    if re.match(r"what can you do", message) or re.match(r"what do you do", message):
        functionality()

    # remove stopwords
    for word in new_tokens:
        if word in stopwords:
            new_tokens.remove(word)

    # get the sentiment score from the user
    score = sia.polarity_scores(message)

    # print out their likes and dislikes if asks for them by the user
    for item in pos_tags:
        if (item[1] == "WP" or item[1] == "WDT") and ("it" not in message):
            if score['compound'] > 0:
                print("Karl> Here are a list of your likes:")
                print(likes)
                if len(likes) > 2:
                    return_message = "LOTS OF LIKES"
                else:
                    return_message = "LITTLE LIKES"
                skip = True
            elif score['compound'] < 0:
                print("Karl> Here are a list of your dislikes:")
                print(dislikes)
                if len(dislikes) > 2:
                    return_message = "LOTS OF DISLIKES"
                else:
                    return_message = "LITTLE DISLIKES"
                skip = True

    # if theres a keyword in the message but it is not asking for the users likes and dislikes
    if not skip and ("like" in message or "dislike" in message or "love" in message or "hate" in message or "favorite" in message):
        # Find users likes and dislikes if they inputted that in
        if score['compound'] > 0:
            if "love" in message:
                item = message[message.find("love"):].replace("love", "").strip()
            elif "like" in message:
                item = message[message.find("like"):].replace("like", "").strip()
            else:
                item = message[message.find("favorite"):].replace("favorite", "").replace("is ", "").strip()
            likes.append(item)
            return_message += "LIKES"
            skip = True
        elif score['compound'] < 0:
            if "hate" in message:
                item = message[message.find("hate"):].replace("hate", "").strip()
            else:
                item = message[message.find("like"):].replace("like", "").strip()
            dislikes.append(item)
            return_message += "DISLIKES"
            skip = True

    if (type(tokens[-1]) == (int or float)) and ("i am" in message or "im" in message):
        return_message = "IM " + tokens[-1] + " YEARS OLD"
        skip = True

    if "joke" in message:
        return_message = "JOKE"
        skip = True

    # get the bird names to match
    if not skip:
        with open(os.path.join(dataPath, 'birdnames.set'), 'r') as file:
            # lowercase everything and remove the dashes in the bird names
            bird_names = file.read().lower().replace("-", " ")
            bird_names = set(tokenize(bird_names))

            # if the user is looking for a bird see what they want to know about the bird
            if not find:
                for item in food_words:
                    # print(pairing[1])
                    if item in message:
                        return_message += "food "
                        find = True
                        break
            if not find:
                for item in life_words:
                    if item in message:
                        return_message += "life "
                        find = True
                        break
            if not find:
                for item in size_words:
                    if item in message:
                        return_message += "size "
                        find = True
                        break
            if not find:
                for item in about_words:
                    if item in message:
                        return_message += "about "
                        break

            # look for bird names in the users message. If the user did enter a bird name add it to the return message
            for word in new_tokens:
                if word in bird_names:
                    return_message += word + " "
                    newPronoun = True

            # remember the pronoun for last time if it is a new pronoun
            if newPronoun:
                pronoun = return_message.split(maxsplit=1)[1]



            # if they gave a pronoun, replace the pronoun with the bird name so the bot can understand
            for pairing in pos_tags:
                if pairing[1] == "PRP" and pairing[0] != "me":
                    return_message += pronoun

    # if the user didn't ask about a bird then return the original message or
    # say anything about their likes and dislikes
    if return_message == "":
        return_message = TreebankWordDetokenizer().detokenize(tokens)

    return return_message.strip(), pronoun, likes, dislikes


#############################################################################################################
#  * Function:            tokenize
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/04/2022
#  *
#  * Description:
#  * Tokenizes the message
#############################################################################################################
def tokenize(string):
    return nltk.word_tokenize(string)


#############################################################################################################
#  * Function:            removePunctuation
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/07/2022
#  *
#  * Description:
#  * Remove the punctuation from the message
#############################################################################################################
def removePunctuation(string):
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in string:
        if ele in punctuation:
            string = string.replace(ele, "")
    return string


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/07/2022
#  *
#  * Description:
#  * Creates a list of POS tags to analyze
#############################################################################################################
def pos(tokens):
    return nltk.pos_tag(tokens)

#############################################################################################################
#  * Function:            token_lemmatize
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/07/2022
#  *
#  * Description:
#  * Lemmatizes the words so that it can be a bit more consistent
#############################################################################################################
def token_lemmatize(tokens):
    newTokens = list()
    for word in tokens:
        newTokens.append(lemmatizer.lemmatize(word))
    return newTokens


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        04/01/2022
#  *
#  * Description:
#  * Main purpose is to check for arguments and start main function
#  *
#  * Parameters:
#############################################################################################################
if __name__ == '__main__':
    main()

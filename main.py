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
import nltk
import pickle
from Person import Person
from nltk.corpus import stopwords
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk.sentiment import SentimentIntensityAnalyzer

stopwords = set(stopwords.words('english'))

# setup the save directory
basePath = r"".join(os.getcwd())  # get the current directory
dataPath = r"".join(os.path.join(basePath, 'data'))

sia = SentimentIntensityAnalyzer()


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
    chatLog = os.path.join(basePath, "chat.log")
    userFile = os.path.join(basePath, "user.pickle")

    notExit = True

    kernel = aiml.Kernel()

    likes = list()
    dislikes = list()
    sessionId = 1234

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

    if os.path.exists(userFile):
        with open(userFile, "rb") as file:
            user = pickle.load(file)
            if user.getName() is not None:
                print(user.getName())
                kernel.setPredicate("username", user.getName())
            if user.getAge() is not None:
                kernel.setPredicate("age", user.getAge())
            likes = user.getLikes()
            dislikes = user.getDislikes()

    intro()

    pronoun = ""

    with open(chatLog, 'w') as log:
        while notExit:
            message = input("user> ").lower()

            log.write("user> " + message + r"\n")

            if message == "quit":
                with open(userFile, "wb") as file:
                    username = kernel.getPredicate("username")
                    age = kernel.getPredicate("age")
                    user = Person(name=username, age=age, likes=likes, dislikes=dislikes)
                    pickle.dump(user, file)
                    print("Bot> User file saved")
                    print("Bot> Goodbye " + username)
                    notExit = False

            elif message == "save":
                kernel.saveBrain("bot_brain.brn")

            else:
                message, pronoun, newLikes, newDislikes = processMessage(message, pronoun, likes, dislikes)

                bot_response = kernel.respond(message)
                print("Bot> " + bot_response + "\n")
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
    print("\n\nBot> Hi my name is Karl. I'm a bird bot.")
    print("Bot> Here are the list of bird species I know:")
    print("     Northern Cardinal            American Goldfinch")
    print("     Northern Mockingbird         House Finch")
    print("     Mourning Dove                Carolina Chickadee")
    print("     White-winged Dove            Carolina Wren")
    print("     Great-tailed Grackle         Blue Jay")
    print("     Yellow-rumped Warbler        Barn Swallow")
    print("     House Sparrow                Eastern Phoebe")
    print("     Ruby-crowned Kinglet")
    print("\nBot> You can ask me about their diet, size and lifespan")
    print("Bot> I can also give you a random fact about a bird")
    print("Bot> I also know a couple of jokes if you're into that.")
    print("Bot> Type \"quit\" anytime to close me")
    print("Bot> Lets start with you. Tell me about yourself like your name, age, and/or likes and dislikes.")


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def functionality():
    print("\n\nBot> Here are the list of bird species I know:")
    print("     Northern Cardinal            American Goldfinch")
    print("     Northern Mockingbird         House Finch")
    print("     Mourning Dove                Carolina Chickadee")
    print("     White-winged Dove            Carolina Wren")
    print("     Great-tailed Grackle         Blue Jay")
    print("     Yellow-rumped Warbler        Barn Swallow")
    print("     House Sparrow                Eastern Phoebe")
    print("     Ruby-crowned Kinglet")
    print("\nBot> You can ask me about their diet, size and lifespan or a general fact")
    print("Bot> I can also give you a random fact about any bird. Just ask for a random bird fact!")
    print("Bot> I also know a couple of jokes if you're into that.")
    print("Bot> Type \"quit\" anytime to close me")


#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def processMessage(message, pronoun, likes, dislikes):
    message = removePunctuation(message)
    tokens = tokenize(message)
    new_tokens = list(tokens)
    pos_tags = pos(new_tokens)
    return_message = ""
    newPronoun = False
    skip = False
    find = False

    # set of topics about a word to match and look for
    size_words = {"size", "big", "large", "width", "dimensions", "long"}
    life_words = {"live"}
    food_words = {"eat", "food", "diet"}
    about_words = {"about", "facts", "fact"}

    # if the user asks what the bot can do
    if re.match(r"what can you do", message) or re.match(r"what do you do", message):
        functionality()

    for word in new_tokens:
        if word in stopwords:
            new_tokens.remove(word)

    # print out their likes and dislikes if asks for them by the user
    for item in pos_tags:
        if item[1] == "WP" and "it" not in message:
            score = sia.polarity_scores(message)
            if score['neg'] < score['pos']:
                print("Bot> Here are a list of your likes:")
                print(likes)
                skip = True
            elif score['neg'] > score['pos']:
                print("Bot> Here are a list of your dislikes:")
                print(dislikes)
                skip = True


    if not skip and "like" in message or "dislike" in message or "love" in message or "hate" in message:
        score = sia.polarity_scores(message)
        # Find users likes and dislikes if they inputted that in
        if score['neg'] < score['pos']:
            if "love" in message:
                item = message[message.find("love"):].replace("love", "").strip()
            else:
                item = message[message.find("like"):].replace("like", "").strip()
            dislikes.append(item)
            return_message += "DISLIKES"
            skip = True
        elif score['neg'] > score['pos']:
            if "hate" in message:
                item = message[message.find("hate"):].replace("hate", "").strip()
            else:
                item = message[message.find("like"):].replace("like", "").strip()
            likes.append(item)
            return_message += "LIKES"
            skip = True

    if type(tokens[-1]) == int or float and ("i am" in message or "im" in message):
        return_message = "IM " + tokens[-1] + " YEARS OLD"
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
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
def tokenize(string):
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
def removePunctuation(string):
    punctuation = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in string:
        if ele in punctuation:
            string = string.replace(ele, "")
    return string


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

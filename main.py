import re

import aiml
import os
import logging


def main():
    # setup the save directory
    basePath = r"".join(os.getcwd())  # get the current directory
    dataPath = r"".join(os.path.join(basePath, 'data'))

    BRAIN_FILE = os.path.join(basePath, "bot_brain.brn")

    logger = logging.getLogger()
    logger.setLevel(logging.CRITICAL)

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

    outputBirdList()

    while True:
        message = input("user> ").lower()

        if message == "quit":
            username = kernel.getPredicate("username")
            print("penis: username = " + username)
            exit()

        if askBirdList(message):
            outputBirdList()

        elif message == "save":
            kernel.saveBrain("bot_brain.brn")

        else:
            bot_response = kernel.respond(message)
            print("Bot> " + bot_response)


def outputBirdList():
    print("Bot> Here are the list of species I know:")
    print("Northern Cardinal")
    print("Northern Mockingbird")
    print("Mourning Dove")
    print("White-winged Dove")
    print("Great-tailed Grackle")
    print("Yellow-rumped Warbler")
    print("House Sparrow")
    print("Ruby-crowned Kinglet")
    print("Eastern Phoebe")
    print("Barn Swallow")
    print("Blue Jay")
    print("Carolina Wren")
    print("Carolina Chickadee")
    print("House Finch")
    print("Orange-crowned Warbler")
    print("Red-winged Blackbird")
    print("American Goldfinch")
    print("Painted Bunting")
    print("European Starling")
    print("Red-bellied Woodpecker")

def askBirdList(message):
    return re.match("what * of birds *", message) or re.match("give a * of bird.", message) or re.match("list * birds", message)


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
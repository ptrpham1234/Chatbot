#############################################################################################################
#  * Function:            main
#  * Author:              Peter Pham (pxp180041)
#  * Date Started:        03/20/2022
#  *
#  * Description:
#  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
#  * the crawl functions that pull data from the birds page and collects more links to traverse
#############################################################################################################
class Person:

    #############################################################################################################
    #  * Function:            main
    #  * Author:              Peter Pham (pxp180041)
    #  * Date Started:        03/20/2022
    #  *
    #  * Description:
    #  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
    #  * the crawl functions that pull data from the birds page and collects more links to traverse
    #############################################################################################################
    def __init__(self, name=None, age=None, grade=None, likes=None, dislikes=None):
        self.name = name
        self.age = age
        self.grade = grade

        if likes is None:
            self.likes = list()
        self.likes = likes

        if dislikes is None:
            self.dislikes = list()
        self.dislikes = dislikes

    #############################################################################################################
    #  * Function:            main
    #  * Author:              Peter Pham (pxp180041)
    #  * Date Started:        03/20/2022
    #  *
    #  * Description:
    #  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
    #  * the crawl functions that pull data from the birds page and collects more links to traverse
    #############################################################################################################
    def addLikes(self, new_likes):
        self.likes.append(new_likes)

    #############################################################################################################
    #  * Function:            main
    #  * Author:              Peter Pham (pxp180041)
    #  * Date Started:        03/20/2022
    #  *
    #  * Description:
    #  * Controls the flow of data process the home page and grabs all of the links related to birds. Then calls
    #  * the crawl functions that pull data from the birds page and collects more links to traverse
    #############################################################################################################
    def addDislikes(self, new_dislikes):
        self.dislikes.append(new_dislikes)

    def getName(self):
        # if the string is empty
        if not self.name:
            return None
        return self.name

    def getAge(self):
        # if the string is empty
        if not self.age:
            return None
        return self.age

    def getLikes(self):
        return self.likes

    def getDislikes(self):
        return self.dislikes

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
    def __init__(self, Name=None, birthday=None, age=None, grade=None):
        self.Name = Name
        self.birthday = birthday
        self.age = age
        self.grade = grade

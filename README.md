# InternshalaWeb

This repository is a collection of the Webscraping done to collect all the names of players who have ever played an ODI mamtch, 
to collect their nationality, and the runs made by each of them in the interval of 1970 -2019 ,and the overall score made by them
in this period.

My code is divided into three python files instead of one , the reason being to increase the efficiency of the program and to reduce overall
computation time. I can guarantee that this will be quite fast , in my case , the whole web scraping took  only _*2 and a halfhours*_ .

The *details of execution of the python files* are in this order :

* cricket.py :generates all links and names of all players who have ever played an ODI.
* cricket2.py :retrieves links from a txt file and processes them to generate the required data in the form of a json file.
* toExcel.py :converts the json file to a csv file for better visualisation.The csv file contains the headers as Name ,Nationality, years … ., and overall_score.





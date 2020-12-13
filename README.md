# Dealroom_internship_assignment

The instructions, data set and results are provided in the Data_Science_Internship_Assignment_Answer.xlsx file.

Three Python scripts are provided among other files :
* part1_clustering.py : This file needs keywords_extractor.py to work.  
  Perform the clustering over the Data sheet in the Excel file. 
* keywords_extractor.py : This file is called in part1_clustering.py.  
  It extracts the keywords of sentences. A keyword is defined as a Noum Phrase (NP). It also applies NLP technics to "clean" the keywords.
* part2_scrapping.py : This file needs the chrome driver to work.  
  It scraps the website https://www.ycombinator.com/companies/ and keeps the following information : name of the company, legend, description, website link, year of creation, team size and	location.
* chromedriver.exe : Chrome version 87. Please check your Chrome version and download the appropriate driver : https://sites.google.com/a/chromium.org/chromedriver/downloads
* requirements.txt : package requirements for the three Python files.

The Python scripts work under Python 3.6+.

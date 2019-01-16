Project: News Data Extraction

Libraies used:
	- Flask
	- oauth2client
	- requests
	- gspread
	- Google App Script


Project Structure:
	- flaskmain.py: Main file of the Flask application. It has functionality defined for all the routes.
	- mainfile.py: This file contains the necessary function of getting the news data and writing to the Google Spreadsheet.
	- articles.py: This class has the strucure defined for the news articles. Currently it has fields like:
		- article_title: Title of the article
		- article_author: Author of the Article
		- article_source: Source of the Article
		- article_url: url of hte article
		- article_published_date: Published date of the article
		- article_brief: Brief description about the article.

	- gspreadapi.py: This file contains the basic functionality to connect to the Google Spreadsheet, getting the workbook and worksheet and writing to the worksheet. The 'write' fuction currently takes the list of Python dictionaries of the news article to write to the Spreadsheet.

	- newsapi.py: This file contains the functionality to set the url, headers and the other parameters of the request, fetch the data using the News API, and filter the data returned in json format to list Python dictionaries.

	- Code.gs: This is a Google App Script file and contains code to create a trigger, call the Flask API using the GET method and Log the messages returned.

Python Code:
	- Flask is used to create an interface which can accept an input 'company name' in this case.
	- This 'input' is used to retieved the News for the past 30 days using the Google News API.
	- The python code then connects to the Google Spreadsheet and writes the News data to the Spreadsheet
	- This Flask code is then deployed on the Google Cloud


Google App Script code: [Code.gs]
	Google App Script code is used to call the Flask based API and specify the search term using the 'GET' method which in turn makes the Python code connect to Spreadsheet and write the News data. The code in the Google App script can be triggerd using a time based trigger to run everyday.

Configuration file[config.json]:
	This file contains the configuration for the Google News API and the Google Spreadsheet API.

	Google Spreadsheet configuration:
		- SERVICE_ACCOUNT_FILE_PATH: path to google service account file
		- WORKBOOK_ID: ID of the workbook to write the data to

	News API configuration:
		- API_KEY: api key for the Google news API
		- URL: "https://newsapi.org/v2/everything"
		- PAGE_SIZE": Size of the page or maximum number of news article which can be extracted in a single API call. Max value id 100
		- NUM_DAYS": Number of days backward from the current day to get the news data for.
		- HEADERS: request headers

Working:
	- Google App Script in Code.gs file has a trigger which calls the 'main' function everyday. 
	- This main function reads the first column of the 'Sheet1' of Active workbook to get the company names. Each cell in Column 'A' in Sheet1 corresponds to 1 company.
	- For each company the Flask API is called. The Flask server is deployed on Google Cloud.
	- Flask API calls the Python code which fetches the news data using the Google NewsAPI and writes to the one worksheet of the workbook specified by config file.
	- The data is fetched and written one page at a time to the worksheet
	- The rows of the worksheet are dynamically increased by keeping track of the number of rows written.

Current Limitations:
	- API key currently being used in the project only allows the past 30 days news search. A maxumum of 100 news articles can be retrieved in a single API call. The page number parameter of the API call need to be incremented by 1 to retrieve next set of 100 articles. The free version of API key allows only 10 pages of news access which means we can access a maximum of 1000 news articles using the free version of the API.

	- Each sheet in Google Spreadsheet can have a finite value of number of rows which is 1000000. Increasing rows beyong this raises an exception which needs to be handled. So, the maximum number of news which can be accomodated in a single sheet cannot increase the maximum of rows. This is not handled. Possible solution can be to create a new page and write the data once the original page reaches its maximum capacity.

	- Currently the responses with status code OTHER THAN 200 are treated similarly with 1 retry mechanism to fetch the data.



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Project Name"        :   "NewsData"                                  #
# "File Name"           :   "mainfile2"                                 #
# "Author"              :   "rishabhzn200"                              #
# "Date of Creation"    :   "Jan-10-2019"                               #
# "Time of Creation"    :   "07:01"                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import requests
import ast
from datetime import datetime as dt, timedelta
import json
import logging
from newsapi import *
from articles import *
from gspreadapi import *
import sys


def get_dates(number_of_days=30):
    """

    :param number_of_days: number of days (backward) from the present day
    :return: start date and the end date
    """
    end = dt.strptime(str(dt.today().date()), "%Y-%m-%d")
    start = end - timedelta(days=number_of_days)
    return str(start.date()), str(end.date())

def get_news(news_list):
    """

    :param news_list: list of news articles
    :return: list of news containing only title, author, source, name, published date and content of the news
    """

    articles = []
    for news in news_list:
        title = news.get('title', None)
        author = news.get('author', None)
        source = news.get('source', None)
        if source is not None:
            source = source.get('name', None)
        url = news.get('url', None)
        published_date = news.get('publishedAt', None)
        brief = news.get('content', None)

        article = Article()
        article.set_articles_values(title=title, author=author, source=source, url=url, date=published_date,
                                    content=brief)
        articles.append(article.get_article())

    return articles


def get_log_message_and_clear(log_messages):
    msgs = log_messages[:]
    log_messages.clear()
    return msgs


def main(query_string):
    """

    :param query_string: query parameter to search for.
    :return: generator of messages(Success/Failure). Side effect of this function is to update the Google Spreadsheet
    """

    # Variable to hold and 'yield' the log messages
    log_messages = []

    # Initialize the configuration
    with open('./config.json', 'r') as f:
        config = json.load(f)

    # News API
    url = config['NEWS_API']['URL']
    headers = config['NEWS_API']['HEADERS']
    search_term = query_string
    start_date, end_date = get_dates()
    pageSize = config['NEWS_API']['PAGE_SIZE']
    page = '1'
    apikey = config['NEWS_API']['API_KEY']
    num_days = config['NEWS_API']['NUM_DAYS']

    # Google Spreadsheet Configuration
    service_account_file = config['GOOGLE_SPREADSHEET']['SERVICE_ACCOUNT_FILE_PATH']
    workbook_id = config['GOOGLE_SPREADSHEET']['WORKBOOK_ID']
    worksheet_name = search_term.upper()


    # Get NewsAPI object
    newsapi = NewsAPI()
    newsapi.set_url(url)
    newsapi.set_headers(headers)
    newsapi.set_params(q=search_term, from_=start_date, to=end_date, pageSize=pageSize, page=page, apikey=apikey, clear_others=False)

    # Initial call to get the number of results
    api_news, status, total_results = newsapi.get_news()
    log_messages.append(f'page={page}\tlen={len(api_news)}')

    if total_results == None:
        log_messages.append("Can't determine the number of pages. Returning from the function")
        #TODO added yield. Original return
        yield get_log_message_and_clear(log_messages)
        return None
    else:
        yield get_log_message_and_clear(log_messages)

    # Number of Pages = (total_results / 100) + 1
    numPages = (total_results // eval(pageSize)) + 1


    # Get the spreadsheet
    # Get the required fields from the news_list
    # news = get_news(news_list)

    # Access the worksheet

    # Get google sheet object
    gapi = GoogleSheetAPI()
    gapi.connect(service_account_file)  # check after this

    workbook = gapi.get_workbook(workbook_id=workbook_id)
    sheet = gapi.get_worksheet(workbook_name=workbook, worksheet_name=worksheet_name)  # , rows=total_results)
    num_rows_in_sheet = 2
    start_row = 1
    sheet.resize(num_rows_in_sheet)

    # Write the news of Page 1


    #End

    # Start from Page 1
    for page in range(1, numPages + 1):
        newsapi.set_params(page=page, clear_others=False)
        api_news, status, total_results = newsapi.get_news()

        if status != 200:
            # Retry Once more
            log_messages.append(f'Failed: page={page}\tstatus={status}. Retrying')
            yield get_log_message_and_clear(log_messages)
            api_news, status, total_results = newsapi.get_news()
            if status != 200:
                log_messages.append(f'Failed Retry: page={page}\tstatus={status}. Moving to next Page')
                yield get_log_message_and_clear(log_messages)
                continue
        else:
            log_messages.append(f'Success: page={page}\tstatus={status}\tlen={len(api_news)}')
            yield get_log_message_and_clear(log_messages)

        if len(api_news) == 0:
            log_messages.append(f"Empty News List for page={page}. Unknown Reason")
            yield get_log_message_and_clear(log_messages)

        # print(f'page={page}\tlen={len(api_news)}')

        # for generator
        yield get_log_message_and_clear(log_messages)

        # TODO change to api_news from news_list
        news = get_news(api_news)

        try:
            num_rows_in_sheet += len(news)

            #TODO check for max resize number
            sheet.resize(num_rows_in_sheet)

            # Write the header if start row is 1
            if start_row == 1:
                num_rows_written = gapi.write_data(sheet, news, start_row=start_row, write_header=True)
            else:
                num_rows_written = gapi.write_data(sheet, news, start_row=start_row, write_header=False)
            start_row += num_rows_written
        except gspread.exceptions.APIError as response:
            log_messages.append("Stopped Due to Error in GSpread")
            yield get_log_message_and_clear(log_messages)
            # print(response)

    return None


# if __name__ == "__main__":
#     query_string = 'Facebook'
#     for msg in main(query_string):
#         print(msg)

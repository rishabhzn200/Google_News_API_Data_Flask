# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Project Name"        :   "NewsData"                                  #
# "File Name"           :   "newsapi.py"                                #
# "Author"              :   "rishabhzn200"                              #
# "Date of Creation"    :   "Jan-03-2019"                               #
# "Time of Creation"    :   "17:04"                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import ast
from security import safe_requests

class NewsAPI:

    def __init__(self, url=None, headers=None, params=None):
        self.url = url
        self.headers = headers
        if params == None:
            self.params = {}

    def set_url(self, url):
        """

        :param url: URL of the News API
        :return: None
        """
        self.url = url

    def set_headers(self, headers):
        """

        :param headers: headers in python dictionary format
        :return: None
        """
        self.headers = headers

    def set_params(self, q=None, from_=None, to=None, pageSize=None, page=None, apikey=None, clear_others=False):
        """

        :param q: query string
        :param from_: start date
        :param to: end date
        :param pageSize: total number of pages to retrieve in 1 API call
        :param page: page number to retrieve
        :param apikey: News API KEY
        :param clear_others: flag which controls if the parameters which were not passed were to retain their original value
        :return: None
        """
        if q != None:
            self.params['q'] = q
        else:
            if clear_others:
                self.params.pop('q', None)

        if from_ != None:
            self.params['from'] = from_
        else:
            if clear_others:
                self.params.pop('from', None)

        if to != None:
            self.params['to'] = to
        else:
            if clear_others:
                self.params.pop('to', None)

        if pageSize != None:
            self.params['pageSize'] = pageSize
        else:
            if clear_others:
                self.params.pop('pageSize', None)

        if page != None:
            self.params['page'] = page
        else:
            if clear_others:
                self.params.pop('page', None)

        if apikey != None:
            self.params['apikey'] = apikey
        else:
            if clear_others:
                self.params.pop('apikey', None)


    # def set_page(self, page=None):
    #     if page != None:
    #         self.params['page'] = page

    def process_news(self, data, **kwargs):
        """

        :param data: data retrieved from the API in string format
        :param kwargs: words to replace. These are usually :None, :true and :False. This is done to convert json formatted string to Python dictionary
        :return: list of dictionary. Each dictionary is a news article.
        """

        # Pre-Process
        for key, value in kwargs.items():
            data = data.replace(key, value)

        # Evaluate
        data = ast.literal_eval(data)  # It is a list

        return data

    def get_news(self):
        """

        :return: news_list_all, response.status_code, total_results: list of news, status code of the request and number of results present
        """
        # May be run a loop to fetch all the news or use generator

        response = safe_requests.get(self.url, headers=self.headers, params=self.params)

        # If status code is not 200(OK), return the empty list for news, the status code and number of results as None
        if response.status_code != 200:
            # Something went wrong
            return [], response.status_code, None

        data = response.text
        processed_data = self.process_news(data, **{':null': ':None', ":true": ':True', ":false": ':False'})
        news_list_all = processed_data.get('articles', None)
        total_results = processed_data.get('totalResults', None)

        return news_list_all, response.status_code, total_results




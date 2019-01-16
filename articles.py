# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Project Name"        :   "NewsData"                                  #
# "File Name"           :   "articles"                                  #
# "Author"              :   "rishabhzn200"                              #
# "Date of Creation"    :   "Jan-03-2019"                               #
# "Time of Creation"    :   "17:09"                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import requests
import ast
import gspreadapi as gapi

class Article:

    def __init__(self):
        self.article_title = None
        self.article_author = None
        self.article_source = None
        self.article_url = None
        self.article_published_date = None
        self.article_brief = None

    def set_articles_values(self, title=None, author=None, source=None, url=None, date=None, content=None):
        """

        :param title: title of the Article
        :param author: Author of the Article
        :param source: Source of the Article
        :param url: URL of the Article
        :param date: Published date of the Article
        :param content: brief description about the Article
        :return: None
        """
        self.article_title = title
        self.article_author = author
        self.article_source = source
        self.article_url = url
        self.article_published_date = date
        self.article_brief = content

    def get_article(self):
        """

        :return: dictionary of the Article
        """
        return self.__dict__




# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# "Project Name"        :   "NewsData"                                  #
# "File Name"           :   "gspreadapi"                                #
# "Author"              :   "rishabhzn200"                              #
# "Date of Creation"    :   "Jan-03-2019"                               #
# "Time of Creation"    :   "17:10"                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #


import gspread
from oauth2client.service_account import ServiceAccountCredentials
from string import ascii_uppercase as au

class GoogleSheetAPI:

    def __init__(self):
        self.gc = None

    def connect(self, service_account_file=None):
        """

        :param service_account_file: path of service account file for Google Account
        :return:
        """
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account_file, scope)

        self.gc = gspread.authorize(credentials)


    def get_workbook(self, workbook_id=None):
        """

        :param workbook_id: id of the workbook in string to search for
        :return: workbook handler
        """
        workbook = self.gc.open_by_key(workbook_id)
        return workbook

    def get_worksheet(self, workbook_name=None, worksheet_name='default', rows=1000, cols=200):
        """

        :param workbook_name: workbook handler
        :param worksheet_name: Name of the worksheet
        :param rows: Number of rows for this worksheet. It can be updated later using resize
        :param cols: Number of colomns for this worksheet
        :return: worksheet handler
        """
        new_worksheet = None
        try:
            new_worksheet = workbook_name.add_worksheet(title=worksheet_name, rows=rows, cols=cols)
        except:
            new_worksheet = workbook_name.worksheet(worksheet_name)

        return new_worksheet

    def update_row(self, worksheet, row_data, row_num, col_start, col_end):
        """

        :param worksheet: Worksheet name
        :param row_data: list of items to be written in a single row
        :param row_num: current row number to write the data to
        :param col_start: Start column
        :param col_end: End Column
        :return:
        """
        cell_list = worksheet.range(f'{col_start}{row_num}:{col_end}{row_num}')
        for cell, data in zip(cell_list, row_data):
            cell.value = data
        try:
            worksheet.update_cells(cell_list)
        except gspread.exceptions.APIError as response:
            raise gspread.exceptions.APIError(response)


    def write_data(self, worksheet, data, start_row=1, write_header=False):
        """

        :param worksheet: Worksheet name
        :param data: list of dictionaries with each dictionary containing the keys and corresponding value
        :param start_row: Row number from where to start writing the data to the worksheet
        :param write_header: boolean value which indicates whether to write header to the Spreadsheet
        :return: returns the number of rows written
        """

        print(f'Inside Function. Start Row = {start_row}')
        if len(data) == 0:
            return 0

        num_cols = len(data[0].keys())
        row = start_row
        col_start = au[0]
        col_end = au[num_cols-1]

        # If write_header is True, write the header and increment the row
        if write_header == True:
            # Update title
            row_data = data[0].keys()
            self.update_row(worksheet, row_data, row, col_start, col_end)



        for data_dict in data:
            row = row + 1
            row_data = data_dict.values()
            try:
                self.update_row(worksheet, row_data, row, col_start, col_end)
            except gspread.exceptions.APIError as response:
                # Return because of exception in GSpread API limits
                raise gspread.exceptions.APIError(response)
            pass
        return (row - start_row)






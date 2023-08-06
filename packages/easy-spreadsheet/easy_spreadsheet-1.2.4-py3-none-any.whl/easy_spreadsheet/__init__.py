import time
import logging
import base64
import json
import itertools
import gspread
import os
import sys
import importlib
import pandas as pd
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials


class EasySpreadsheet():
    
    def __init__(self, auth_json: dict, spreadsheet_id: str, sheet_name: str, load=True):


        self.table = None

        self._spread_order = list(self._allcombinations(
            'ABCDEFGHIJKLMNOPQRSTVWXYZ', minlen=1, maxlen=2))
        self._doc = self._get_doc(auth_json, spreadsheet_id)
        self._sheet_name = sheet_name
        self._cloudsheet= None
        if load:
            self._load()
    
    def select(self):
        return self.table
    
    def push(self):
        
        cell_list = []
        for index, row in self.table.iterrows():
            values = self._make_sheet_row(row)
            
            for value_index, value in enumerate(values):
                cell = gspread.models.Cell(index + 1, value_index + 1)
                cell.value = value
                cell_list.append(cell)

        self._cloudsheet.clear()
        self._cloudsheet.update_cells(cell_list)
        
    def format(self, start_column, start_index, end_column, end_index, cell_format):
        
        range_name = self._spread_order[start_column] + str(start_index + 1) + ":" + \
                    self._spread_order[end_column] + str(end_index + 1)

        return self._cloudsheet.format(range_name, cell_format)

    def load_from_another_sheet(self, sheet):
        self.table = sheet.table.copy()

    def _allcombinations(self, alphabet, minlen=1, maxlen=None):
        thislen = minlen
        while maxlen is None or thislen <= maxlen:
            for prod in itertools.product(alphabet, repeat=thislen):
                yield ''.join(prod)
            thislen += 1

    def _get_doc(self, auth_json, spreadsheet_id):
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
            'https://spreadsheets.google.com/feeds',
        ]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(
            auth_json, scopes)
        gc = gspread.authorize(credentials)
        spreadsheet_url = f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=0'
        doc = gc.open_by_url(spreadsheet_url)

        return doc

    def _load(self):

        self._cloudsheet = self._doc.worksheet(self._sheet_name)
        records = self._cloudsheet.get_all_values()
        rows = []
        for row in records:
            temp = []
            for p in row:
                v = self._parse(p)
                temp.append(v)

            rows.append(temp)

        self.table = pd.DataFrame(rows)
        

    def _convert_to_str(self, value):
        if type(value) is list or type(value) is dict:
            v = json.dumps(value, ensure_ascii=False)
        else:
            v = str(value)

        return v

    def _parse(self, value):
        try:
            if type(value) is list or type(value) is dict:
                v = value
            elif len(value) != 0 and (value[0] == "{" or value[0] == "["):
                v = json.loads(value)
            else:
                v = str(value)
        except:
            v = str(value)

        return v

    def _make_sheet_row(self, row):
        temp = []
        for p in row:
            v = self._convert_to_str(p)

            temp.append(v)

        return temp

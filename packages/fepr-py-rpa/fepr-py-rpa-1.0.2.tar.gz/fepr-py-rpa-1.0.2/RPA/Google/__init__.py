from googleapiclient.discovery import build
import pickle
import os
import pandas as pd


class SpreadsheetMetadata(object):
    def __init__(self, index: list, sheet_type: list, sheet_title: list, sheet_id: list):
        self.index = index
        self.sheet_types = sheet_type
        self.sheet_titles = sheet_title
        self.sheet_ids = sheet_id

    @property
    def sheet_meta_dict(self) -> list:
        meta_dict: dict = {}
        meta_list: list = []
        for i in range(len(self.sheet_titles)):
            meta_dict['id'] = self.sheet_ids[i]
            meta_dict['title'] = self.sheet_titles[i]
            meta_dict['index'] = self.index[i]
            meta_dict['type'] = self.sheet_types[i]
            meta_list.append(meta_dict.copy())

        return meta_list


class Spreadsheet(object):
    def __init__(self):
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                cred = pickle.load(token)
        self.spreadsheet = build('sheets', 'v4', cache_discovery=False, credentials=cred).spreadsheets()

    def get_table(self, spreadsheet_id: str, range_: str) -> pd.DataFrame:
        result = self.spreadsheet.values().get(
            spreadsheetId=spreadsheet_id, range=range_).execute()
        values = result.get('values', [])
        sheet = pd.DataFrame(values, columns=values[0])
        sheet = sheet.drop(0)
        sheet = sheet.reset_index()
        return sheet

    def get_values(self, spreadsheet_id: str, range_: str) -> list:
        result = self.spreadsheet.values().get(
            spreadsheetId=spreadsheet_id, range=range_).execute()
        values = result.get('values', [])
        return values

    def set_dataframe(self, spreadsheet_id: str, range_: str, dataframe):
        self.spreadsheet.values().append(spreadsheetId=spreadsheet_id,
                                         valueInputOption="USER_ENTERED",
                                         range=range_,
                                         body={"values": dataframe.values.tolist()}).execute()

    def set_values(self, spreadsheet_id: str, range_: str, values):
        self.spreadsheet.values().update(spreadsheetId=spreadsheet_id,
                                         valueInputOption="USER_ENTERED",
                                         range=range_,
                                         body={"values": [[values]]}).execute()

    def get_metadata(self, spreadsheet_id: str) -> SpreadsheetMetadata.sheet_meta_dict:
        sheet_metadata = self.spreadsheet.get(
            spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')

        sheet_title_list = [Sheet_Name["properties"]["title"]
                            for Sheet_Name in sheets]

        sheet_index_list = [Sheet_index["properties"]["index"]
                            for Sheet_index in sheets]

        sheet_id_list = [Sheet_id["properties"]["sheetId"]
                         for Sheet_id in sheets]

        sheet_type_list = [Sheet_type["properties"]["sheetType"]
                           for Sheet_type in sheets]
        metadata = SpreadsheetMetadata(sheet_index_list, sheet_type_list, sheet_title_list, sheet_id_list)
        return metadata.sheet_meta_dict

import datetime
import json
import sys

import pandas as pd


class ExcelAnalyzer:
    def __init__(self, file_path: str):
        self.sub_data = None
        self.file_path = file_path
        self.max_row = 0
        self.max_col = 0
        self.size = 0
        self.base_keyword = None
        self.base_position = (0, 0)
        self.xlsx = pd.ExcelFile(self.file_path)
        self.sheet_names = self.xlsx.sheet_names
        self.clean_data = {
            'campaign': {
                'data': [],
                'interest': []
            },
        }

    def __call__(self, *args, **kwargs):
        self.find_keyword_in_sheets(['campaign', 'interest rate'])

    @staticmethod
    def get_value_with_index(df: pd.DataFrame, row: int, col: int) -> str or None:
        if row is not None and col is not None:
            value = df.iloc[row, col]

            # validate type datetime to format string
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y/%m/%d')
            return value

    def get_info_data(self, df: pd.DataFrame, row: int, col: int):
        # find size data of main keyword (campaign, interest rate)
        for index in range(1, self.max_row):
            # handle error index out of bounded (max row)
            current_index = row + index
            self.size = index - 1
            if current_index == self.max_row:
                break

            text = self.get_value_with_index(df, current_index, col)
            if pd.isna(text) or pd.isnull(text):
                break

        get_row_info = df.iloc[row]

        if self.base_keyword == 'campaign':
            proc_key = list(self.sub_data.keys())
        else:
            self.sub_data = {}
            proc_key = get_row_info.dropna().tolist()

        found = get_row_info[get_row_info.isin(proc_key)]
        for index, name in enumerate(found.tolist()):
            col = df.columns.get_loc(found.index[index])
            self.sub_data[name] = (row, col)

    def export_to_json(self, index):
        with open(f'{index + 1}.json', 'w') as outfile:
            json.dump(self.clean_data, outfile)

    def find_keyword_in_sheets(self, keywords: list):
        for sheet_idx in range(len(self.sheet_names)):
            self.sub_data = {'filename': 0, 'effdate': 0, 'remark': 0}
            df = pd.read_excel(self.xlsx, sheet_name=self.sheet_names[sheet_idx])
            for keyword in keywords:
                self.base_keyword = keyword
                result = df.where(df == keyword).stack().reset_index()
                self.max_row, self.max_col = df.shape

                for _, row in result.iterrows():  # O(1)
                    col_idx = df.columns.get_loc(row['level_1'])
                    row_idx = row['level_0']
                    self.get_info_data(df, row_idx, col_idx)

                self.scan_data(df)

            # export data
            self.export_to_json(sheet_idx)

    def scan_data(self, df: pd.DataFrame):
        bash = []
        save_at = ''
        for i in range(1, self.size + 1):
            prepare_data = {}

            if self.base_keyword == 'campaign':
                for name, (row, col) in self.sub_data.items():
                    prepare_data[name] = self.get_value_with_index(df, row + i, col)
                save_at = 'data'
                bash.append(prepare_data)
            else:
                data = []
                if not bash:
                    bash.append(list(self.sub_data.keys()))
                for name, (row, col) in self.sub_data.items():
                    data.append(self.get_value_with_index(df, row + i, col))
                save_at = 'interest'
                bash.append(data)

        self.clean_data['campaign'][save_at] = bash


if __name__ == "__main__":
    file = sys.argv[1]

    analyzer = ExcelAnalyzer(file)
    analyzer()

import csv
import json
import os
from pathlib import Path
import spacy


class Knowledge:
    nlp = spacy.load("fr_core_news_sm")

    def __init__(self, knowledge: dict):
        self.data = knowledge

    def get_optimized_dic(self):
        dic = {}
        for key, values in self.data.items():
            for value, element in values.items():
                for e in element:
                    dic[e] = (key, value)

        return dic

    def lemmatiz_data(self):
        for _class, item in self.data.items():
            for value, syns in item.items():
                self.data[_class][value] = [Knowledge.get_lemma(syn) for syn in syns]

    @staticmethod
    def get_lemma(text: str):
        doc = Knowledge.nlp(text.lower())
        result = " ".join([token.lemma_ for token in doc])

        return result

    @staticmethod
    def __csv_to_dict(filepath: str) -> dict:
        dic = {}
        with open(filepath) as f:
            reader = csv.reader(f)
            headers = next(reader)
            for row in reader:
                dic[row[0]] = [value for value in row[1:] if value != '']
                dic[row[0]] += [value for value in row[1:] if value != '' and value != '...' and value != value]
                dic[row[0]] += [row[0]]

        filename = Path(filepath).name

        return {filename[:-4]: dic}

    @staticmethod
    def __json_to_dict(filepath: str) -> dict:
        with open(filepath) as f:
            dic = json.load(f)

        return dic

    @staticmethod
    def csv_file_factory(filepath: str):
        dic = Knowledge.__csv_to_dict(filepath)
        instance = Knowledge(dic)

        return instance

    @staticmethod
    def csv_folder_factory(folder_path: str):
        dic = {}
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        for file in files:
            dic.update(Knowledge.__csv_to_dict(f"{folder_path}{file}"))

        instance = Knowledge(dic)

        return instance

    @staticmethod
    def json_file_factory(filepath: str):
        dic = Knowledge.__json_to_dict(filepath)
        instance = Knowledge(dic)

        return instance

    @staticmethod
    def json_folder_factory(folder_path: str):
        dic = {}
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

        for file in files:
            dic.update(Knowledge.__json_to_dict(f"{folder_path}{file}"))

        instance = Knowledge(dic)

        return instance

    def dump_json(self, folder_path: str = "", one_file_by_key: bool = True):

        if not os.path.isdir(f"{folder_path}/data"):
            os.makedirs(f"{folder_path}data")

        if one_file_by_key:
            for key, values in self.data.items():
                with open(f"{folder_path}data/{key}.json", "w", encoding='utf8') as outfile:
                    json.dump({key: values}, outfile, indent=4, ensure_ascii=False)
        else:
            with open(f"{folder_path}data/data.json", "w", encoding='utf8') as outfile:
                json.dump(self.data, outfile, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    pass

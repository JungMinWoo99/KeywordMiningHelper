import csv
import pandas as pd


def csv_to_dict(file_name="word_dict.csv"):
    csv_data = pd.read_csv(file_name)
    csv_data.columns = ['word', 'count']
    csv_list = csv_data.to_dict('list')
    word_dict = {}
    # csv_list를 딕셔너리로 변환
    for idx in range(len(csv_list['word'])):
        word_dict[csv_list['word'][idx]] = csv_list['count'][idx]

    return word_dict


def dict_to_csv(input_dict, file_name="word_dict.csv"):
    with open(file_name, 'w', encoding='UTF-8') as f:
        dict_series = pd.Series(input_dict)
        data = pd.DataFrame(dict_series)
        data.to_csv(file_name)

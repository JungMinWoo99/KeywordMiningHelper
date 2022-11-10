from kiwipiepy import Kiwi, basic_typos
import re


def is_noun(word_token):
    """
    일반 명사와 고유 명사만 추출

    :param word_token:
    :return:
    """
    if word_token.tag == "NNG" or \
            word_token.tag == "NNP":
        return True
    else:
        return False


def get_string_from_text(file_name):
    """
    파일로 부터 문자열을 가져옴

    :param file_name:
    :return:
    """
    file = open(file_name, 'rt', encoding='UTF8')
    str_list = file.readlines()
    return str_list


def remove_blank_from_str_list(str_list):
    """
    문자열의 줄바꿈 문자를 지움
    url문자열에 섞인 이스케이프 문자 삭제용

    :param str_list:
    :return:
    """
    for idx in range(0, len(str_list)):
        str_list[idx] = re.sub("\n", "", str_list[idx])


class KeywordMiner:

    def __init__(self):
        """
        키워드 추출을 위해 필요한 객체 생성
        """
        self.kiwi = Kiwi(typos=basic_typos, model_type='sbg')
        self.keyword_dict = {}

    def word_extraction_from_str_list(self, text_str_list, max_word_len=10, min_cnt=0):

        # 문장에서 새로운 단어를 찾아 사전에 추가
        self.kiwi.extract_add_words(texts=text_str_list, min_cnt=1, max_word_len=max_word_len)

        # 문장 분석
        analyze_res_list = self.kiwi.analyze(text=text_str_list)

        # 문장 분석 후 키워드 딕셔너리 생성
        for analyze_res in analyze_res_list:
            for str_info in analyze_res:
                for word_info in str_info[0]:
                    if is_noun(word_info) is False:
                        continue
                    if len(word_info.form) > max_word_len:
                        continue
                    if self.keyword_dict.get(word_info.form) is None:
                        self.keyword_dict[word_info.form] = 1
                    else:
                        self.keyword_dict[word_info.form] += 1

        # 최소 빈도수 보다 적은 수의 단어 삭제
        self.remove_word_from_dict(min_cnt=min_cnt)

    def remove_word_from_dict(self, min_cnt):
        """
        최소 빈도수 보다 적은 수의 단어는 삭제

        :param min_cnt: 최소 빈도수
        :return:
        """
        if min_cnt <= 1:
            return
        else:
            for key in self.keyword_dict:
                if self.keyword_dict[key] < min_cnt:
                    del self.keyword_dict[key]

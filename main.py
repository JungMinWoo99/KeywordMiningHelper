import matplotlib.pyplot as plt
import numpy as np
import re
from PIL import Image
from kiwipiepy import Kiwi, basic_typos
from wordcloud import WordCloud, ImageColorGenerator
from url_handler import *


def is_noun(word_token):
    if word_token.tag == "NNG" or \
            word_token.tag == "NNP":
        return True
    else:
        return False


def get_string_from_text(file_name):
    file = open(file_name, 'rt', encoding='UTF8')
    str_list = file.readlines()
    return str_list


def remove_blank_from_str_list(str_list):
    for idx in range(0, len(str_list)):
        str_list[idx] = re.sub("\n", "", str_list[idx])


class KeywordMiner:

    def __init__(self):
        self.kiwi = Kiwi(typos=basic_typos, model_type='sbg')
        self.keyword_dict = {}

    def word_extraction_from_str_list(self, text_str_list, min_cnt, max_word_len):

        # 문장에서 새로운 단어를 찾아 사전에 추가
        self.kiwi.extract_add_words(texts=text_str_list, min_cnt=min_cnt, max_word_len=max_word_len)

        # 문장 분석
        analyze_res_list = self.kiwi.analyze(text=text_str_list)

        # 문장 분석후
        for analyze_res in analyze_res_list:
            for str_info in analyze_res:
                for word_info in str_info[0]:
                    if is_noun(word_info) is False:
                        continue
                    if self.keyword_dict.get(word_info.form) is None:
                        self.keyword_dict[word_info.form] = 1
                    else:
                        self.keyword_dict[word_info.form] += 1


class WordcloudGenerator:

    def __init__(self, word_dict, font_path='C:\Windows\Fonts\malgunbd.ttf', mask_image_path=None, coloring_opt=False):
        # 이미지 마스크 설정
        if mask_image_path is not None:
            self.mask = self.mask = np.array(Image.open(mask_image_path))
        else:
            self.mask = None

        # 컬리링 설정(단어의 색깔을 이미지의 색과 맞춤)
        # 주의 사항: 배경은 무조건 255값의 완전 하얀색이여야함
        if coloring_opt is True:
            self.image_colors = ImageColorGenerator(self.mask)

        self.wordcloud_obj = WordCloud(background_color="white", font_path=font_path, mask=self.mask)
        self.wordcloud = self.wordcloud_obj.generate_from_frequencies(word_dict)

    def create_wordcloud(self):
        plt.figure(figsize=(16, 8))
        plt.imshow(self.wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()

    def create_wordcloud_coloring(self):
        fig, axes = plt.subplots(1, 3)
        axes[0].imshow(self.wordcloud, interpolation='bilinear')
        axes[1].imshow(self.wordcloud.recolor(color_func=self.image_colors), interpolation='bilinear')
        axes[2].imshow(self.mask, cmap=plt.cm.gray, interpolation='bilinear')
        for ax in axes:
            ax.set_axis_off()
        plt.show()


url_list = get_string_from_text(file_name="url_list.txt")
remove_blank_from_str_list(url_list)
text_list = text_extract_from_res_obj_list(get_urls_in_request(url_list))
miner = KeywordMiner()
# file_name_input = input()
# file_name_input = 'test2.txt'
# miner.word_extraction_from_str_list(get_string_from_text(file_name=file_name_input), min_cnt=0, max_word_len=20)
miner.word_extraction_from_str_list(text_list, min_cnt=0, max_word_len=20)
print(miner.keyword_dict)
wcgen = WordcloudGenerator(word_dict=miner.keyword_dict, mask_image_path='images3.png', coloring_opt=True)
wcgen.create_wordcloud_coloring()

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator


class WordcloudGenerator:

    def __init__(self, word_dict, font_path='C:\Windows\Fonts\malgunbd.ttf', mask_image_path=None, coloring_opt=False,
                 background_color="white", colormap="viridis", wc_width=400, wc_height=200, wc_scale=1):
        """
        워드 클라우드 생성을 위한 설정
        
        :param word_dict: 단어 딕셔너리
        :param font_path: 사용할 폰트 파일의 경로
        :param mask_image_path: 마스킹시 사용할 이미지 경로
        :param coloring_opt: Image-colored wordcloud 설정
        :param background_color: 사용하는 이미지의 배경색
        """
        # 이미지 마스크 설정
        self.coloring_opt = False
        if mask_image_path is not None:
            self.mask = self.mask = np.array(Image.open(mask_image_path))
            if coloring_opt is True:
                # 컬리링 설정(단어의 색깔을 이미지의 색과 맞춤)
                # 주의 사항: 배경은 무조건 255값의 완전 하얀색이여야함
                self.image_colors = ImageColorGenerator(self.mask)
                self.coloring_opt = True
            else:
                self.coloring_opt = False
        else:
            self.mask = None

        # 워드클라우드 객체 생성
        self.wordcloud_obj = WordCloud(background_color=background_color, font_path=font_path, mask=self.mask,
                                       width=wc_width, height=wc_height, scale=wc_scale, colormap=colormap)
        self.wordcloud = self.wordcloud_obj.generate_from_frequencies(word_dict)

    def create_wordcloud(self):
        """
        워드 클라우드 생성
        :return:
        """
        plt.figure(figsize=(16, 8))
        if self.coloring_opt is False:
            # not Image-colored wordcloud
            plt.imshow(self.wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()
        else:
            # Image-colored wordcloud
            plt.imshow(self.wordcloud.recolor(color_func=self.image_colors), interpolation='bilinear')
            plt.axis("off")
            plt.show()

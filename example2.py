import url_handler as uh
import text_handler as th
import word_cloud_generator as wcg

#상위 url로 부터 하위 url목록 가져오기
super_url_list = th.get_string_from_text(file_name="super_url_list.txt")
sub_url_list = uh.link_extract_from_res_obj_list(uh.get_urls_in_request(super_url_list))

# url 목록의 url로 부터 텍스트를 가져옴
text_list = uh.text_extract_from_res_obj_list(uh.get_urls_in_request(super_url_list))

# keywordminer객체 생성
miner = th.KeywordMiner()

# url로부터 가져온 텍스트 목록에서 키워드 추출(최대 단어 길이 = 20, 최소 빈도수 = 0)
miner.word_extraction_from_str_list(text_list, min_cnt=0, max_word_len=20)

# 단어 분포를 텍스트 파일로 저장(추후 엑셀 파일로 변경 예정)
file = open("ext_res.txt", 'wt', encoding='UTF8')
file.write(miner.keyword_dict.__str__())

# 추출한 키워드로 워드클라우드 생성(mask_image_path: 사용할 이미지 파일, coloring_opt: 사진의 색깔에 맞게 단어 색을 입히는 옵션)
wcgen = wcg.WordcloudGenerator(word_dict=miner.keyword_dict,
                               mask_image_path='images4.jpg',
                               coloring_opt=False,
                               wc_height=3200, wc_width=6400, wc_scale=10,
                               colormap="flag")
wcgen.create_wordcloud()

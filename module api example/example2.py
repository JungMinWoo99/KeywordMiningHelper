import url_handler as uh
import text_handler as th
import word_cloud_generator as wcg


# 상위 url로 부터 하위 url목록 가져오기(해당 파일에 상위 url 입력)
super_url_list = th.get_string_from_text(file_name="super_url_list.txt")
sub_url_list = uh.link_extract_from_res_obj_list(uh.get_urls_in_request(super_url_list))

# 키워드 추출 객체
miner = th.KeywordMiner()

# url을 5개씩 처리(한꺼번에 여러개 처리시 오버플로우 발생)
cnt = 0
while cnt != len(sub_url_list):
    url_list = []
    if (cnt+5) >= len(sub_url_list):
        url_list = sub_url_list[cnt:]
        cnt = len(sub_url_list)
    else:
        url_list = url_list = sub_url_list[cnt:cnt+5]
        cnt += 5
    # url에서 텍스트 추출
    text_from_url = uh.text_extract_from_res_obj_list(uh.get_urls_in_request(url_list))

    # 텍스트로 부터 키워드 추출
    miner.word_extraction_from_str_list(text_from_url)

# 단어 분포를 텍스트 파일로 저장(추후 엑셀 파일로 변경 예정)
file = open("ext_res.txt", 'wt', encoding='UTF8')
file.write(miner.keyword_dict.__str__())

# 추출한 키워드로 워드클라우드 생성(mask_image_path: 사용할 이미지 파일, coloring_opt: 사진의 색깔에 맞게 단어 색을 입히는 옵션)
wcgen = wcg.WordcloudGenerator(word_dict=miner.keyword_dict,
                               mask_image_path='image.png',
                               coloring_opt=False,
                               wc_height=1000, wc_width=1000, wc_scale=10,
                               colormap="flag")
wcgen.create_wordcloud()

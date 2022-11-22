import tkinter
import tkinter.ttk
import url_handler as uh
import text_handler as th
import csv_handler as ch
import word_cloud_generator as wcg
import matplotlib.colors as mcolors

# 설정 상수
image_path_opt = "image.png"
url_list_file_path_opt = "url_list.txt"

# 화면 구성 요소
window = tkinter.Tk()
window.title("Keyword Mining Helper")
window.geometry("900x660")
window.resizable(False, False)

# 키워드 추출
miner = th.KeywordMiner()

# 콤보 박스에 사용할 리스트
colormap_list = wcg.plt.colormaps()
colormap_list.sort()
by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))), name) for name, color in mcolors.CSS4_COLORS.items())
background_color_list = [x[1] for x in by_hsv]


def add_url():
    url = url_input.get("1.0", "end-1c")

    if url:
        url_list_box.insert(tkinter.END, url)
        url_input.delete("1.0", "end")


def extract_sub_url():
    url = url_input.get("1.0", "end-1c")
    super_url_list = [url]

    if url:
        url_input.delete("1.0", "end")
        sub_url_list = uh.link_extract_from_res_obj_list(uh.get_urls_in_request(super_url_list))
        for sub_url in sub_url_list:
            url_list_box.insert(tkinter.END, sub_url)


def load_url_text_file():
    url_list = th.get_string_from_text(file_name=url_list_file_path_opt)
    th.remove_blank_from_str_list(url_list)
    for sub_url in url_list:
        url_list_box.insert(tkinter.END, sub_url)


def remove_url():
    current_select_url = url_list_box.curselection()

    if url_list_box.size() > 0 and current_select_url:
        url_list_box.delete(current_select_url[0])


def clear_url():
    while url_list_box.size() > 0:
        url_list_box.delete(tkinter.END)


def mining_keyword():
    # url 리스트 박스에서 url 리스트 얻기
    if url_list_box.size() == 0:
        return

    # url을 5개씩 처리
    cnt = 0
    while cnt != url_list_box.size():
        url_list = []
        if (cnt+5) >= url_list_box.size():
            url_list = list(url_list_box.get(cnt, url_list_box.size() - 1))
            cnt = url_list_box.size()
        else:
            url_list = list(url_list_box.get(cnt, cnt+4))
            cnt += 5
        # url에서 텍스트 추출
        text_from_url = uh.text_extract_from_res_obj_list(uh.get_urls_in_request(url_list))

        # 텍스트로 부터 키워드 추출
        miner.word_extraction_from_str_list(text_from_url)

    # 트리뷰 비우기
    for i in word_distribute_box.get_children():
        word_distribute_box.delete(i)

    # 추출한 텍스트를 분포수 기준으로 정렬하여 단어 분포에 입력
    word_tuple_list = list(zip(miner.keyword_dict.keys(), miner.keyword_dict.values()))
    word_tuple_list.sort(key=lambda x: x[1], reverse=True)
    for word in word_tuple_list:
        word_distribute_box.insert('', 'end', text=word[0], values=word[1], iid=word[0])


def remove_word():
    current_select_word_tuple = word_distribute_box.selection()
    word_list = [current_select_word_tuple[0]]
    miner.remove_word_from_dict(del_list=word_list)
    word_distribute_box.delete(current_select_word_tuple[0])


def filter_min():
    min_num = min_num_input.get("1.0", "end-1c")
    if min_num:
        min_num_input.insert(tkinter.END, min_num)
        min_num_input.delete("1.0", "end")
        if min_num.isdecimal():
            miner.remove_word_from_dict(min_cnt=int(min_num))
        word_distribute_box.delete(*word_distribute_box.get_children())
        word_tuple_list = list(zip(miner.keyword_dict.keys(), miner.keyword_dict.values()))
        word_tuple_list.sort(key=lambda x: x[1], reverse=True)
        for word in word_tuple_list:
            word_distribute_box.insert('', 'end', text=word[0], values=word[1], iid=word[0])


def wc_gen():
    image_path = image_path_opt if use_image_check_var.get() == 1 else None
    use_colormap_bool = use_colormap_check_var.get() == 1
    colormap = colormap_combo_box.get() if colormap_combo_box.get() != '' else 'viridis'
    background_color = background_color_combo_box.get() if background_color_combo_box.get() != '' else 'black'
    wc_height = wc_height_input.get("1.0", "end-1c") if wc_height_input.get("1.0",
                                                                            "end-1c") != '' and wc_height_input.get(
        "1.0", "end-1c").isdecimal() else '1000'
    wc_width = wc_width_input.get("1.0", "end-1c") if wc_width_input.get("1.0", "end-1c") != '' and wc_width_input.get(
        "1.0", "end-1c").isdecimal() else '1000'

    wc_generator = wcg.WordcloudGenerator(word_dict=miner.keyword_dict,
                                          mask_image_path=image_path,
                                          coloring_opt=use_colormap_bool,
                                          wc_height=int(wc_height), wc_width=int(wc_width), wc_scale=10,
                                          colormap=colormap,
                                          background_color=background_color)
    wc_generator.create_wordcloud()
    
    # 추출 결과를 csv 파일로도 저장
    ch.dict_to_csv(miner.keyword_dict)


# url 입력
url_label = tkinter.Label(window, text="URL", width=5, height=1)
url_label.place(x=10, y=13)

url_input = tkinter.Text(window, width=80, height=1)
url_input.place(x=50, y=14)

url_add_button = tkinter.Button(window, text="추가하기", width=15, height=1, command=add_url, repeatdelay=1000,
                                repeatinterval=100)
url_add_button.place(x=620, y=10)

extract_sub_url_button = tkinter.Button(window, text="하위 URL 추출", width=15, height=1, command=extract_sub_url,
                                        repeatdelay=1000, repeatinterval=100)
extract_sub_url_button.place(x=740, y=10)

# url 목록 출력
url_list_label = tkinter.Label(window, text="URL 목록", width=10, height=1)
url_list_label.place(x=1, y=50)

url_list_box = tkinter.Listbox(window, width=80, height=20)
url_list_box.place(x=10, y=70)

load_url_text_file_button = tkinter.Button(window, text="URL 텍스트 파일 로드", width=20, height=1, command=load_url_text_file,
                                           repeatdelay=1000, repeatinterval=100)
load_url_text_file_button.place(x=600, y=80)

remove_url_button = tkinter.Button(window, text="삭제하기", width=20, height=1, command=remove_url, repeatdelay=1000,
                                   repeatinterval=100)
remove_url_button.place(x=600, y=120)

clear_url_button = tkinter.Button(window, text="초기화", width=20, height=1, command=clear_url, repeatdelay=1000,
                                  repeatinterval=100)
clear_url_button.place(x=600, y=160)

mining_keyword_button = tkinter.Button(window, text="키워드 추출", width=20, height=1, command=mining_keyword,
                                       repeatdelay=1000, repeatinterval=100)
mining_keyword_button.place(x=600, y=200)

# 단어 분포 결과 출력
word_distribute_label = tkinter.Label(window, text="단어 분포", width=7, height=1)
word_distribute_label.place(x=10, y=400)

word_distribute_box = tkinter.ttk.Treeview(window, height=10, columns=["one"], displaycolumns=["one"])
word_distribute_box.place(x=10, y=420)

word_distribute_box.column("#0", width=200, )
word_distribute_box.heading("#0", text="단어")

word_distribute_box.column("#1", width=200, anchor="center")
word_distribute_box.heading("one", text="분포수", anchor="center")

keyword_del_button = tkinter.Button(window, text="단어 삭제", width=15, height=1, command=remove_word, repeatdelay=1000,
                                    repeatinterval=100)
keyword_del_button.place(x=430, y=450)

min_num_input = tkinter.Text(window, width=5, height=1)
min_num_input.place(x=560, y=493)

min_filter_button = tkinter.Button(window, text="최소빈도필터", width=15, height=1, command=filter_min, repeatdelay=1000,
                                   repeatinterval=100)
min_filter_button.place(x=430, y=490)

min_filter_button = tkinter.Button(window, text="워드 클라우드 생성", width=15, height=1, command=wc_gen, repeatdelay=1000,
                                   repeatinterval=100)
min_filter_button.place(x=430, y=530)

# 워드 클라우드 이미지 옵션
image_option_label = tkinter.Label(window, text="이미지 옵션", width=10, height=1)
image_option_label.place(x=650, y=400)

background_color_label = tkinter.Label(window, text="배경색", width=5, height=1)
background_color_label.place(x=650, y=430)
background_color_combo_box = tkinter.ttk.Combobox(textvariable=str, width=20)
background_color_combo_box['value'] = background_color_list
background_color_combo_box.place(x=700, y=430)

colormap_label = tkinter.Label(window, text="컬러맵", width=5, height=1)
colormap_label.place(x=650, y=460)
colormap_combo_box = tkinter.ttk.Combobox(textvariable=str, width=20)
colormap_combo_box['value'] = colormap_list
colormap_combo_box.place(x=700, y=460)

use_image_check_var = tkinter.IntVar()
use_image_check_button = tkinter.ttk.Checkbutton(variable=use_image_check_var)
use_image_check_button.config(text="이미지 사용")
use_image_check_button.place(x=650, y=490)

use_colormap_check_var = tkinter.IntVar()
use_colormap_check_button = tkinter.ttk.Checkbutton(variable=use_colormap_check_var)
use_colormap_check_button.config(text="이미지 컬러링 사용")
use_colormap_check_button.place(x=650, y=520)

wc_width_label = tkinter.Label(window, text="사진 폭", width=10, height=1)
wc_width_label.place(x=650, y=550)
wc_width_input = tkinter.Text(window, width=15, height=1)
wc_width_input.place(x=750, y=550)

wc_height_label = tkinter.Label(window, text="사진 높이", width=10, height=1)
wc_height_label.place(x=650, y=580)
wc_height_input = tkinter.Text(window, width=15, height=1)
wc_height_input.place(x=750, y=580)

# 화면 실행

window.mainloop()

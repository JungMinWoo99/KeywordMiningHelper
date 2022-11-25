# KeywordMiningHelper
- 웹페이지의 텍스트로부터 키워드를 추출하고 워드 클라우드로 시각화 하여 보여주는 파이썬 프로그램입니다.
<br><br>

## 시작하기

### 사전 준비 요소

시작하기 전에 다음 요소가 설치되어 있어야 합니다.
- [Python 3.x](https://www.python.org/)
- [Git](https://git-scm.com/)

### 패키지 설치

시작하기 전에 다음 명령어를 통해 필요한 패키지를 설치합니다.
```powershell
> python.exe -m pip install --upgrade pip
> pip install kiwipiepy
> pip install matplotlib
> pip install wordcloud
> pip install beautifulsoup4
> pip install pandas
```

### 프로젝트 소스 코드 얻기

위의 절차를 완료했으면, 명령어를 입력하여 프로젝트의 소스 코드를 얻습니다.
```powershell
> git clone https://github.com/KeywordMiningHelper/KeywordMiningHelper
```

### 프로그램 실행

소스 코드를 얻었으면 다음 명령어를 통해 프로그램을 실행합니다.  
- `client.py`파일 직접 실행하면 명령어 없이 바로 GUI 프로그램을 사용할 수 있습니다.
```powershell
> cd KeywordMiningHelper
> python client.py
```
<br><br>


## 사용 방법

GUI 화면에서 프로그램을 사용하는 방법에 대한 설명입니다.  

### URL 입력

URL **에서 키워드 추출**
1. URL입력창에 URL을 넣고 추가를 합니다.
2. 필요한 URL를 모두 입력했다면 키워드 추출 버튼을 누릅니다.
3. 트리뷰에 키워드 분포결과가 나옵니다.

**텍스트 파일 로드**

1. 파일내의 url_list.txt에 url목록을 추가합니다.
2. 필요한 URL 을 모두 입력했다면 파일을 저장하고 텍스트 파일 로드 버튼을 누릅니다.
3. URL 목록창에 URL 들이 추가되었음을 확인 할 수 있습니다.

**하위 url추출**
**※ 주의: 너무 많은 url을 입력하면 키워드 추출에 매우 오랜 시간이 걸립니다.**

1. URL 입력창에 하위URL 을 추출할 상위 URL을 입력합니다.
2. 입력후 하위 URL 추출 버튼을 누릅니다.
3. URL 목록에서 하위 URL 목록을 확인 할 수 있습니다.


### 키워드 분포 설정

**키워드 삭제**
- 트리뷰에서 삭제를 원하는 단어를 누르고 삭제하기버튼을 눌러 삭제할 수 있습니다.

**최소 빈도수 설정**
- 추출 결과에서 일정 갯수를 못넘은 단어를 일괄적으로 지울 수 있습니다.
1. 최소 빈도수에 원하는 수치를 입력합니다.
2. 최소 빈도수 버튼을 누르면 입력한 수치 미만의 단어는 목록에서 지워집니다.

### 워드 클라우드 생성

워드 클라우드를 생성하는 방법들 입니다.  
배경색은 `Matplotlib`의 named colors, 컬러맵은 `Matplotlib`의 Colormaps을 사용합니다.  
- [List of named colors - Matplotlib 3.6.2 documentation](https://matplotlib.org/stable/gallery/color/named_colors.html)
- [Choosing Colormaps in Matplotlib - Matplotlib 3.6.2 documentation](https://matplotlib.org/stable/tutorials/colors/colormaps.html)

**이미지 틀없이 워드 클라우드 생성**
1. 이미지 설정에서 사진의 크기와 배경색, 컬러맵을 설정합니다.
2. 워드 클라우드 생성 버튼을 누릅니다.

**이미지 틀을 사용하여 워드 클라우드 생성**
1. 사용하는 이미지를 `image.png`이름으로 프로그램 폴더에 저장합니다. (이때 이미지의 배경색이 RGB값이 모두 255인 하얀색이여야 합니다.)
2. 이미지 틀 사용 체크박스를 누르고 배경색과 컬러맵을 선택합니다.
3. 워드클라우드 생성버튼을 누릅니다.

**이미지 컬러링으로 워드 클라우드 생성**
1. 이미지 틀을 사용한 방법에서 추가로 이미지 컬러링 체크박스를 누릅니다.
2. 워드클라우드 생성 버튼을 누르면 이미지 컬러링이 된 워드 클라우드를 확인 할 수 있습니다.

### CSV파일 생성

워드클라우드를 만들때 사용한 단어 분포 정보는 워드클라우드 생성시 파일에 `word_dict.csv`로 저장됩니다.  
해당 파일을 통해 단어 분포 정보를 다른 곳에서도 사용할 수 있습니다.  
<br><br>


## 제공 기능

기본적으로 GUI를 제공하지만 기능별로 나눠진 파이썬 파일을 통해 구현된 기능을 부분적으로 사용가능합니다.

### `url_handler.py`
- `beautifulsoup4`을 통해 웹페이지에서 텍스트와 URL 링크를 분리하는 기능이 구현되어 있습니다.

### `text_handler.py`
- `kiwipiepy`를 통해 텍스트의 형태소를 분석하고 원하는 형태소만 추출하는 기능이 구현되어 있습니다.

### `csv_handler.py`
- panda를 통해 딕셔너리를 csv로, csv를 딕셔너리로 변환하는 기능이 구현되어 있습니다.

### `word_cloud_generator.py`
- 워드클라우드를 생성하는 객체가 구현되어 있습니다. GUI 에서 제공하지 않는 세부설정(ex폰트)를 사용 할 수 있습니다.
<br><br>

## 라이센스

### **kiwipiepy : LGPL v3** 
- [Kiwi/LICENSE at main · bab2min/Kiwi](https://github.com/bab2min/Kiwi/blob/main/LICENSE)

### **pandas : BSD 3-Clause License**
- [pandas/LICENSE at main · pandas-dev/pandas](https://github.com/pandas-dev/pandas/blob/main/LICENSE)

### **word_cloud: MIT**
- [word_cloud/LICENSE at master · amueller/word_cloud](https://github.com/amueller/word_cloud/blob/master/LICENSE)

### **beautifulsoup4: MIT**
- [Beautiful Soup Documentation - Beautiful Soup 4.9.0 documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.html?highlight=license)

### **Matplotlib**
- [License - Matplotlib 3.6.2 documentation](https://matplotlib.org/stable/users/project/license.html)

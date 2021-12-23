# anaconda, 파이썬 설치
# C드라이브 하위에 프로젝트 폴더 생성
# 해당 디렉토리에서 cmd 열고 명령어 python -m venv C:\imtora_provider
# 확장 패키지 python, Code Runner 설치 후 vscode 재실행
# ctrl+shift+p -> python : Select Interfrete -> python('base':conda)
# powershell 열어 다음의 명령어들 실행 
# conda create -n imtora_provider : 아나콘다 가상환경 생성
# conda activate imtora_provider : 생성한 가상환경을 택
# pip install flask : Flask설치 진행
# pip list : Flask 설치 확인
# 프로젝트폴더에서 app.py파일 생성
# 코딩 후 Flask실행 (python app.py / flask run)
# 소스코드에 오류가 있으면 실행되지 X

from flask import Flask
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts='localhost', port=9200)


list= es.indices.get_alias('*')

bodys = {}

app = Flask(__name__) # Flask 모듈을 사용할 수 있게 된다?

# ----------- 학습을 위한 간단한 UI 생성(HTML사용법 in Python) -----------

@app.route('/')
def es_home():
    html = '''
    <ul>
        <a href='get'> get </a><br>
        <a href='filter'> filter </a><br>
        <a href='aggs'> aggregation </a><br>
        <a href='indices.get'> indices.get </a><br>
        <a href='get_alias'> get_alias </a><br>
        <a href='index_list'> index_list </a>
    '''
    return html

# ----------- get : index, id 정보가 일치하는 document(row)들 ------------

@app.route('/get')
def get():
    docs= es.get(index='stations', id='1')
    docs2= docs['_source']
    return docs
    # return docs2

# -------- filter : index, body(query, match) 정보가 맞는 document들 --------

@app.route('/filter')
def filter():
    docs= es.search(index='stations', body={'from':3, 'size':2, 'query':{
        'match':{
            'num':1
        }
    }})
    return docs

# -------- sum집계 : index, body(aggrs, 작명, sum) 모든 값들의 합  ---------

@app.route('/aggs')
def aggs():
    docs= es.search(index='stations', body={'size':0, 'aggs':{
        'sumAggrs':{
            'sum':{
                'field':'num'
            }
        }
    }})
    return docs

# ------------ es.indices.get("*") -------------

@app.route('/indices.get')
def indicesget():
    list2= es.indices.get('*')
    return list2

# ------------ es.indices.get_alias("*") -------------

@app.route('/get_alias')
def alias():
    return list

# ----------- index list 를 불러오기 위해 반복문, if문 활용 ------------

@app.route('/index_list')
def index_list():
    indexHtml=""
    for v in list:
        if v[0]!=".":
            indexHtml+= v+'<br>'

    # 참고: Jason의 타입을 string으로 전환시 "<class dict>" 요상하게 나옴
    print(str(type(list))[3:7]) 

    return indexHtml

    # python에서의 Json은 그 DataType이 'dict'이며 배열처럼 반복문이 가능
    # Json의 반복문의 변수는 key이므로 v[0]= key(문자열)의 첫 문자  

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # debug=True : 소스코드의 변경을 API에 즉각적으로 반영
    # 포트 의미는?
from fastapi import FastAPI
import requests, time

app = FastAPI()

@app.get("/")
def init():
    ts = round(time.time() * 1000)
    url = 'https://zaisen.tid-keisei.jp/kr/data/traffic_info.json?ts=' + str(ts)
    response = requests.get(url)

    # {
    # "id": "U048", //역 id
    # "tr": [{
    #     "no": "582K", //열차번호
    #     "bs": "0",    //선로 번호
    #     "sy": "6",    //0 스카이라이너, 1 모닝라이너, 2 이브닝라이너, 
    #  			        //3 통근특급, 4 특급, 5 급행, 6 보통
	# 			        //11 쾌속, 15 쾌속특급, 17 엑세스 특급
	# 			        //99 정보없음, 16 시티라이너 (운행 중단)
    #     "ik": "90",   //목적지 역 id
    #     "dl": "0",    //지연시간
    #     "hk": "0",    //0 우에노방향, 1 반대방향
    #     "sr": "8"     //량수
    # }]
    # }

    # 역 목록
    stns = [
        # 케이세이 본선
        {"stn":"케이세이우에노 (京成上野)", "id":"001"},{"stn":"닛포리 (日暮里)", "id":"003"},{"stn":"신미카와시마 (新三河島)", "id":"004"},{"stn":"마치야 (町屋)", "id":"005"},{"stn":"센주오하시 (千住大橋)", "id":"006"},{"stn":"케이세이세키야 (京成関屋)", "id":"007"},{"stn":"호리키리쇼부엔 (堀切菖蒲園)", "id":"008"},{"stn":"오하나자야 (お花茶屋)", "id":"009"},{"stn":"아오토 (青砥)", "id":"010"},{"stn":"케이세이타카사고 (京成高砂)", "id":"011"},

        # 나리타공항선 & 호쿠소선
        {"stn":"신시바마타 (新柴又)", "id":"211"},{"stn":"야기리 (矢切)", "id":"140"},{"stn":"키타코쿠분 (堀之内貝塚)", "id":"212"},{"stn":"아키야마 (秋山)", "id":"213"},{"stn":"히가시마츠도 (東松戸)", "id":"148"},{"stn":"마츠히다이 (松飛台)", "id":"214"},{"stn":"오마치 (大町)", "id":"215"},{"stn":"신카마가야 (新鎌ヶ谷)", "id":"141"},{"stn":"니시시로이 (西白井)", "id":"142"},{"stn":"시로이 (白井)", "id":"216"},{"stn":"코무로 (小室)", "id":"149"},{"stn":"치바뉴타운추오 (千葉ニュータウン中央)", "id":"143"},{"stn":"인자이마키노하라 (印西牧の原)", "id":"144"},{"stn":"인바니혼이다이 (印旛日本医大)", "id":"145"},{"stn":"나리타유카와 (成田湯川)", "id":"146"},

        # 케이세이 본선
        {"stn":"공항제2빌딩 (空港第2ビル)", "id":"044"},{"stn":"나리타공항 (成田空港)", "id":"045"}
    ]

    # 종점 목록
    terms = {
        '1': '우에노',
        '45': '나리타 공항'
    }

    result = []
    for stn in stns:
        result.append({
            'stn': stn['stn'],
            'up': [],
            'dn': []
        })

    data = response.json()
    for i in range(len(result)):

        if data['TS']: #역에 열차가 있는 경우 TS
            for e in data['TS']:
                if (e['id'] == 'E' + stns[i]['id']):
                    for train in e['tr']:
                        if train['sy'] != '0': continue # 스카이라이너 필터링
                        ud = 'up'
                        if train['hk'] == '1': ud = 'dn'
                        result[i][ud].append({
                           'terminal': terms[train['ik']],
                           'type': train['sy'],
                           'status': '도착'
                        })
        
        if data['EK']: #역으로 열차가 이동 중인 경우 EK
            for e in data['EK']:
                if (e['id'][1:] == stns[i]['id']):
                    for train in e['tr']:
                        if train['sy'] != '0': continue # 스카이라이너 필터링
                        ud = 'up'
                        if train['hk'] == '1': ud = 'dn'
                        result[i][ud].append({
                           'terminal': terms[train['ik']],
                           'type': train['sy'],
                           'status': '접근'
                        })



    

    return result

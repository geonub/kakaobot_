from .request import Crawl
from hanspell import spell_checker

class Contents():
    def get_stock_contents(self):
        pick_value = Crawl().stock_crawl()
        contents = """실시간 주요 증시 정보입니다

코스피: [시가] {0[0]}
(전일 종가대비 {1[0]})

코스닥: [시가] {0[1]}
(전일 종가대비 {1[1]})

코스피 200: [시가] {0[2]}
(전일 종가대비 {1[2]})

다우존스: [시가] {2[5]}
(전일 종가대비 {3[5]})

나스닥 종합: [시가] {2[6]}
(전일 종가대비 {3[6]})

S&P 500: [시가] {2[7]}
(전일 종가대비 {3[7]})

상해 종합: [시가] {2[1]}
(전일 종가대비 {3[1]})

니케이 225: [시가] {2[0]}
(전일 종가대비 {3[0]})

영국 FTSE: [시가] {2[10]}
(전일 종가대비 {3[10]})

독일 DAX30: [시가] {2[11]}
(전일 종가대비 {3[11]})""".format(pick_value[0],pick_value[1],pick_value[2],pick_value[3])
        return contents

    def get_goods_contents(self):
        pick_value = Crawl().goods_crawl()
        contents = """실시간 현물 정보입니다

두바이유: {0[3]}달러/배럴
(기준일 대비 {1[3]})

브렌트유: {0[4]}달러/배럴
(기준일 대비 {1[4]})

서부텍사스유(WTI): {0[5]}달러/배럴
(기준일 대비 {1[5]})

국내 금: {0[6]}원/g
(기준일 대비 {1[6]})

국제 금: {0[7]}달러/트로이온스
(기준일 대비 {1[7]})

백금: {0[8]}달러/트로이온스
(기준일 대비 {1[8]})

은: {0[9]}달러/트로이온스
(기준일 대비 {1[9]})

팔라듐: {0[10]}달러/트로이온스
(기준일 대비 {1[10]})""".format(pick_value[0],pick_value[1])

        return contents

    def get_exchange_contents(self):
        pick_value = Crawl().exchange_crawl()
        contents = """실시간 환율 정보입니다

미국 USD: {0[0]}원 (전일비 {1[0]})

일본 JPY: {0[1]}원 (전일비 {1[1]})

중국 CNY: {0[2]}원 (전일비 {1[2]})

유로 EUR: {0[3]}원 (전일비 {1[3]})

영국 GBP: {0[4]}원 (전일비 {1[4]})

스위스 HKD: {0[5]}원 (전일비 {1[5]})

캐나다 TWD: {0[6]}원 (전일비 {1[6]})

뉴질랜드 NZD: {0[7]}원 (전일비 {1[7]})

홍콩 HKD: {0[8]}원 (전일비 {1[8]})

브라질 BRL: {0[9]}원 (전일비 {1[9]})""".format(pick_value[0],pick_value[1])

        return contents

    def get_want_stock_contents(self,content):
        pick_value = Crawl().wanted_stock_crawl(content)
        contents ="""'{0}'으로 검색한 결과입니다.
결과는 최대 3개까지 표시되므로
원하지 않는 결과가 출력되었다면
조금 더 구체적으로 입력해주세요~
""".format(content)
        for n in range(len(pick_value[0])):
            contents += """
종목명: {0}
현재가: {1[0]}
전일비: {1[4]}
등락률: {1[1]}
거래량: {1[2]}
거래대금: {1[3]}(백만원)
""".format(pick_value[0][n],pick_value[1][n])
        return contents

    def get_spell_contents(self,content):
        result = spell_checker.check(content)
        return result[2]

    def get_typing_mode_contents(self,index):
        contents = [
    """입력 모드로 진입했습니다.
조회하고 싶은 주식 종목을 입력해주세요~

ex) 삼성전자, 셀루메드, 삼양옵틱스

입력 모드에서 빠져나가시려면,
'나가기'라고 입력해주세요.""",

    """py-hanspell
Copyright (c) 2015 SuHun Han
The MIT License (MIT)
네이버 맞춤법 검사기를 이용합니다.

입력 모드로 진입했습니다.
교정하고 싶은 문장을 입력해주세요~

ex) 나는 외안되는데?

입력 모드에서 빠져나가시려면,
'나가기'라고 입력해주세요."""
        ]
        return contents[index]

    def get_rank_contents(self):
        pick_value = Crawl().show_rank()
        contents ="""-1위-
필명: {0[0]}
수익률: {0[2]}
평가금액: {0[3]}원
투자원금: {0[4]}
회전율: {0[5]}
매매일수: {0[6]}

-2위-
필명: {1[0]}
수익률: {1[2]}
평가금액: {1[3]}원
투자원금: {1[4]}
회전율: {1[5]}
매매일수: {1[6]}
""".format(pick_value[0],pick_value[1])
        return contents

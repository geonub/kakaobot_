from bs4 import BeautifulSoup
import requests
from requests.utils import requote_uri
from selenium import webdriver
from pyvirtualdisplay import Display
import time

class Crawl:
    def stock_url(self,target):
        url = "http://finance.daum.net/search/search.daum?page=1&col=foreignrate&order=desc&name="+str(target)
        url = requote_uri(url)
        return url

    def getsoup(self,url):
        target = requests.get(url)
        soup = BeautifulSoup(target.text, "html.parser")
        return soup

    def exchange_crawl(self):
        price_list = self.getsoup("http://finance.daum.net/exchange/exchangeMain.daum?nil_profile=stockgnb&nil_menu=exchange_top").find_all("dd", {"class": "exPrice"})
        price_list = [s.get_text() for s in price_list[0:10]]

        updown_list = self.getsoup("http://finance.daum.net/exchange/exchangeMain.daum?nil_profile=stockgnb&nil_menu=exchange_top").find_all("dd", {"class": "exChange"})
        updown_list = [s.get_text() for s in updown_list[0:10]]
        updown_list = [repr(s).replace("\\xa0",'') for s in updown_list]
        updown_list = [s.replace("▼",'▼ ') for s in updown_list]
        ud_list = []
        for s in updown_list:
            if not "▼" in s:
                s = "▲ {0}".format(s)
                ud_list.append(s)
            else:
                ud_list.append(s)

        ud_list = [s.replace("'",'') for s in ud_list]
        ex_list = [price_list,ud_list]

        return ex_list

    def stock_crawl(self):
        d_price_list = self.getsoup("http://finance.naver.com/sise/").find_all("span", {"class":"num"})
        d_price_list = [s.get_text() for s in d_price_list]

        d_updown_list = self.getsoup("http://finance.naver.com/sise/").find_all("span", {"class":"num_s"})
        d_updown_list = [s.get_text() for s in d_updown_list]
        d_updown_list = [s.replace("\n",'') for s in d_updown_list]
        d_updown_list = [s.replace("상승",'') for s in d_updown_list]
        d_ud_list = []
        for s in d_updown_list:
            if "-" in s:
                s = "▼ {0}".format(s)
                d_ud_list.append(s)
            else:
                s = "▲ {0}".format(s)
                d_ud_list.append(s)

        w_price_list = self.getsoup("http://finance.daum.net/global/index.daum?nil_profile=stockgnb&nil_menu=global_top").find_all("span", {"class":"num1"})
        w_price_list = [s.get_text() for s in w_price_list]
        w_updownvol_list = self.getsoup("http://finance.daum.net/global/index.daum?nil_profile=stockgnb&nil_menu=global_top").find_all("span", {"class":"num2"})
        w_updownvol_list = [s.get_text() for s in w_updownvol_list]
        w_updownvol_list = [s.replace("하락",'▼ ') for s in w_updownvol_list]
        w_updownvol_list = [s.replace("상승",'▲ ') for s in w_updownvol_list]
        w_updownrate_list = self.getsoup("http://finance.daum.net/global/index.daum?nil_profile=stockgnb&nil_menu=global_top").find_all("span", {"class":"num3"})
        w_updownrate_list = [s.get_text() for s in w_updownrate_list]
        w_ud_list = []
        for i in range(0,12):
            s = w_updownvol_list[i] + " " + w_updownrate_list[i]
            w_ud_list.append(s)
        stock_list = [d_price_list, d_ud_list, w_price_list, w_ud_list]

        return stock_list

    def goods_crawl(self):
        raw = self.getsoup("http://info.finance.naver.com/marketindex/?tabSel=gold#tab_section").find_all("td", {"class":"num"})
        raw = [s.get_text() for s in raw]
        raw[-1] = raw[-1].replace(' ','')
        r_updown_list = []
        for i in range(0,32,3):
            a = raw[i+1] +" "+ raw[i+2]
            r_updown_list.append(a)
        r_ud_list = []
        for s in r_updown_list:
            if "-" in s:
                s = "▼{0}".format(s)
            elif "0.00%" in s:
                s = "-{0}".format(s)
            else:
                s = "▲{0}".format(s)
                s = s[0:s.rfind(' ')] + ' +' + s[s.rfind(' ') + 1:]
            r_ud_list.append(s)
        r_price_list = raw[0:32:3]
        goods_list = [r_price_list, r_ud_list]
        return goods_list

    def wanted_stock_crawl(self,target):
        soup = self.getsoup(self.stock_url(target))
        up_down = soup.find_all("td", {"class":"num2"})
        if len(up_down) != 0:
            up_down = [j.get_text() for j in up_down[0:3]]
            up_down = [j.replace(j[0],j[0]+" ") for j in up_down]
            value = soup.find_all("td", {"class":"num"})
            value = [a.get_text() for a in value[0:12]]
            value = [value[i:i+4] for i in range(0, len(value), 4)]
            for i in range(len(up_down)):
                value[i].append(up_down[i])
            name = soup.find_all("td", {"class":"txt"})
            name = [a.get_text() for a in name[0:3]]
        else:
            value_r = soup.find_all("ul", {"class":"list_stockrate"})
            value_r = value_r[0].get_text().splitlines()
            value_r[7] = value_r[7].replace("거래량 ","")
            value_r[7] = value_r[7].replace(value_r[7][-1],"")
            value_r[8] = value_r[8].replace("거래대금 ","")
            value_r[8] = value_r[8].replace(value_r[8][-3:],"")
            if value_r[3][0] =="+":
                value_r[2] = "▲ " + value_r[2]
            elif value_r[3][0] =="-":
                value_r[2] = "▼ " + value_r[2]
            else: value_r[2] = "- " + value_r[2]
            value=[[]]
            value[0].extend([value_r[1],value_r[3],value_r[7],value_r[8],value_r[2]])
            name = [soup.find_all("h2")[3].get_text()]
        return name,value

    def show_rank(self):
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        driver.get('https://www.kiwoom.com/nkw.templateContents.do?url=nkw.LO1009List.do?menu=nkw.nCustChkSub.do?m=m1102050000')
        driver.find_element_by_id('id').send_keys('ghw0125k')
        driver.find_element_by_id('passwd').send_keys('gh0125k')
        driver.find_element_by_id('signchk').click()
        driver.find_element_by_id('m1304010000_login').click()
        time.sleep(0.1)
        try:
            alert = driver.switch_to_alert()
            alert.accept()
        except:
            pass
        driver.implicitly_wait(10)
        driver.get('https://vts2.kiwoom.com/group_g/motu/sooic_stock.asp?contest=3372')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all("tbody")
        get = data[0].get_text()
        ranklist = [get.split('\n')[5:12],get.split('\n')[17:24]]
        driver.quit()
        return ranklist

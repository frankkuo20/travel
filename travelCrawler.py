import csv
import sys

import requests


class Base:
    def __init__(self, page=1, endPage=1):
        self._page = page
        self._endPage = endPage + 1
        self._travelData = []  # 旅遊資料
        self._filghtData = []  # 航班資料

    def run(self):
        for i in range(self._page, self._endPage):
            self.crawler(i)

    def crawler(self, page):  # overridde
        raise NotImplementedError("Must override")

    @property
    def travelData(self):
        return self._travelData

    @property
    def filghtData(self):
        return self._filghtData


class OrangeTravel(Base):
    def __init__(self, page=1, endPage=1):
        super().__init__(page, endPage)

    def crawler(self, page):
        url = 'http://www.orangetour.com.tw/EW/Services/SearchListData.asp'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'displayType': 'G', 'subCd': '', 'orderCd': '',
            'pageALL': page,  # 分頁
            'pageGO': '1', 'pagePGO': '1', 'waitData': 'false', 'waitPage': 'false', 'mGrupCd': '',
            'SrcCls': '', 'tabList': '', 'regmCd': '', 'regsCd': '', 'beginDt': '2019/03/07',
            'endDt': '2019/09/07', 'portCd': '', 'tdays': '', 'bjt': '', 'carr': '',
            'allowJoin': '1', 'allowWait': '1', 'ikeyword': '',
        }
        res = requests.post(url, headers=headers, data=data)
        res = res.json()
        # res['All'] #全部商品, res['Go'] # 團體旅遊, res['Pgo'] #團體自由行
        siteTitle = res['SiteTitle']

        for obj in res['All']:
            row = [siteTitle,
                   obj['GrupCd'], obj['GrupLn'], obj['GrupSnm'], obj['LeavDt'],
                   obj['SaleAm'], obj['SaleYqt'], obj['EstmTotqt'],
                   obj['WeekDay'], obj['FullSts'], obj['SignUpLink'], obj['IsShowGuarantee'],
                   obj['IsShowPromote'], obj['IsShowHotTp'], obj['SubCdAnm'], obj['Url'], obj['ImgUrl']]
            print(siteTitle, obj['GrupCd'])
            self._travelData.append(row)
            self.filghtCrawler(siteTitle, obj['GrupCd'], obj['SacctNo'])

    def filghtCrawler(self, siteTitle, prodCd, sacctNo):
        url = 'http://www.orangetour.com.tw/EW/Services/SearchFlight.asp?prodCd={}&sacctNo={}&flightType=1'
        url = url.format(prodCd, sacctNo)

        res = requests.get(url)
        res = res.json()
        for obj in res['Flights']:
            row = [
                siteTitle,
                obj['ProdCd'], obj['GbookDy'], obj['FltNo'],
                obj['DepDt'], obj['DepTm'], obj['ArrDt'],
                obj['ArrTm'], obj['RoutId'], obj['DepCityNm'],
                obj['ArrCityNm'], obj['DepAirpNm'], obj['ArrAirpNm'],
                obj['CarrNm'],
            ]
            self._filghtData.append(row)


class NewamazingTravel(Base):
    def __init__(self, page=1, endPage=1):
        super().__init__(page, endPage)

    def crawler(self, page):

        url = 'https://www.newamazing.com.tw/EW/Services/SearchListData.asp'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'displayType': 'G', 'subCd': '', 'orderCd': '',
            'pageALL': page,  # 分頁
            'pageGO': '1', 'pagePGO': '1', 'waitData': 'false', 'waitPage': 'false', 'mGrupCd': '',
            'SrcCls': '', 'tabList': '', 'regmCd': '', 'regsCd': '', 'beginDt': '2019/03/07',
            'endDt': '2019/09/07', 'portCd': '', 'tdays': '', 'bjt': '', 'carr': '',
            'allowJoin': '1', 'allowWait': '1', 'ikeyword': '',
        }
        res = requests.post(url, headers=headers, data=data)
        res = res.json()
        # res['All'] #全部商品, res['Go'] # 團體旅遊, res['Pgo'] #團體自由行
        siteTitle = res['SiteTitle']

        for obj in res['All']:
            row = [siteTitle,
                   obj['GrupCd'], obj['GrupLn'], obj['GrupSnm'], obj['LeavDt'],
                   obj['SaleAm'], obj['SaleYqt'], obj['EstmTotqt'],
                   obj['WeekDay'], obj['FullSts'], obj['SignUpLink'], obj['IsShowGuarantee'],
                   obj['IsShowPromote'], obj['IsShowHotTp'], obj['SubCdAnm'], obj['Url'], obj['ImgUrl']]
            self._travelData.append(row)
            print(siteTitle, obj['GrupCd'])
            self.filghtCrawler(siteTitle, obj['GrupCd'], obj['SacctNo'])

    def filghtCrawler(self, siteTitle, prodCd, sacctNo):
        url = 'https://www.newamazing.com.tw/EW/Services/SearchFlight.asp?prodCd={}&sacctNo={}&flightType=1'
        url = url.format(prodCd, sacctNo)

        res = requests.get(url)
        res = res.json()
        for obj in res['Flights']:
            row = [
                siteTitle,
                obj['ProdCd'], obj['GbookDy'], obj['FltNo'],
                obj['DepDt'], obj['DepTm'], obj['ArrDt'],
                obj['ArrTm'], obj['RoutId'], obj['DepCityNm'],
                obj['ArrCityNm'], obj['DepAirpNm'], obj['ArrAirpNm'],
                obj['CarrNm'],
            ]
            self._filghtData.append(row)


class MainApp:
    def __init__(self, page, endPage):
        orangeTravel = OrangeTravel(page, endPage)
        orangeTravel.run()

        newamazingTravel = NewamazingTravel(page, endPage)
        newamazingTravel.run()

        travelCsvPath = 'travel.csv'
        travelHead = ['旅行社',
                      '行程號', '旅遊天數', '行程名稱', '出發日期',
                      '價錢', '可售位', '總團位',
                      '星期', '備註', '報名狀態', '是否保證出團',
                      '是否促銷', '是否額滿', '類型', '旅程連結', '封面圖片連結']
        csvFile = open(travelCsvPath, 'w', newline='')
        csv_file_writer = csv.writer(csvFile)
        csv_file_writer.writerow(travelHead)
        csv_file_writer.writerows(orangeTravel.travelData)
        csv_file_writer.writerows(newamazingTravel.travelData)
        csvFile.close()

        flightCsvPath = 'flight.csv'
        flightHead = ['旅行社',
                      '行程號', '天數', '航班', '起飛日期',
                      '起飛時間', '抵達日期', '抵達時間',
                      'RoutId', '出發城市', '抵達城市', '出發地',
                      '目的地', '航空公司']
        csvFile = open(flightCsvPath, 'w', newline='')
        csv_file_writer = csv.writer(csvFile)
        csv_file_writer.writerow(flightHead)
        csv_file_writer.writerows(orangeTravel.filghtData)
        csv_file_writer.writerows(newamazingTravel.filghtData)
        csvFile.close()


if __name__ == '__main__':

    page = 1
    endPage = page
    if len(sys.argv) == 2:
        page = int(sys.argv[1])
    if len(sys.argv) == 3:
        endPage = int(sys.argv[2])

    MainApp(page, endPage)



# {
#     "GrupCd": "EE1090309QRA", # id unique
#     "LeavDt": "2019/03/09", # 出發日期
#     "WeekDay": "六",  #星期
#     "GrupSnm": "銀色 克斯波 雙5星 雙堡 雙國家公園 OUTLET 10天",  #產品名稱
#     "ItnRk3S": "", # 無使用
#     "EstmYqt": 32, # 有抓 無使用
#     "DoneYqt": 0,  # 無使用
#     "SaleYqt": 31, # 可售
#     "DordQt": 0,   # 無使用
#     "EstmTotqt": 32, # 機位
#     "PortNm": "台北-桃園機場 ", # 無使用
#     "FullSts": "",  #備註？"已成團"
#     "RuleDr": "", <span class=product_concessions> 有用 沒資料
#     "SaleCd": 7, # 無使用
#     "HotTp": "",  # 無使用
#     "GordLk": true, # 無使用
#     "OrderDl": "2019/03/09", # 無使用
#     "HtlOkFg": true, # 無使用
#     "AdvFg": false, # 無使用
#     "GuaranteeFg": false, # 無使用
#     "PromoteFg": false, # 無使用
#     "ApplyQt": 999,  已報名數量  # 未使用
#     "DepositQt": 999,  已收訂
#     "NoDepositQt": 0,  未收訂
#     "RqstQt": 999, # 有抓 無使用
#     "SignUpLink": {  # 按鈕 配合status
#         "Status": 0,
#         "Name": "截止",
#         "Url": ""
#     },
#     "IsShowGuarantee": false,  # bool show 是否保證出團
#     "IsShowPromote": false, # bool show 是否促銷
#     "IsShowHotTp": false,  # bool show HotTpNm
#     "HotTpNm": "",   # 有看到 (push, 滿) 紅色按鈕
#     "RecCnt": 1069, # 無使用
#     "GoCnt": 1069, # 無使用
#     "PgoCnt": 0, # 無使用
#     "RowId": 5, # 無使用
#     "SacctNo": "",  # 太複雜 航班會用到
#     "MgrupCd": "EE004",
#     "SaleAm": 59900, # 促銷金額
#     "AgtAm": 59900,  # if srcCls == 1直客價
#     "GrupLn": 10,  # 旅遊天數
#     "SubCd": "GO", # 類型 class="Go"
#     "SubCdAnm": "團", # 類型 裡的文字
#     "SortSq": 7, # 無使用
#     "Url": "/EW/GO/GroupDetail.asp?prodCd=EE1090309QRA",
#     "ShareUrl": "http://www.orangetour.com.tw/EW/GO/GroupDetail.asp?prodCd=EE1090309QRA", # 無使用
#     "SrcCls": 0,  # 判斷 == 1會有 直客價
#     "ImgUrl": "/eWeb_asiantour/IMGDB/000034/000312/00005679.JPG" # 縮圖模式
# },


# 航班資訊
# http://www.orangetour.com.tw/EW/Services/SearchFlight.asp?prodCd=AE1190307RJA&sacctNo=&flightType=1


# {
#     "ProdCd": "EW1090312CIA",  # id
#     "BookSq": "01",       #
#     "GbookDy": 1,       # 天數
#     "GbookSq": 1,          #無使用
#     "FltNo": "CI075",          #航班
#     "DepDt": "2019/03/12",    #起飛日期
#     "DepTm": "23:40",         #起飛時間
#     "ArrDt": "2019/03/13",    #抵達日期
#     "ArrTm": "07:50",         #抵達時間
#     "RoutId": "TPE/ROM",      #RoutId
#     "DepCityNm": "台北市",     #出發城市
#     "ArrCityNm": "羅馬",       #抵達城市
#     "DepAirpNm": "桃園國際機場",    #出發地
#     "ArrAirpNm": "羅馬機場",       # 目的地
#     "CarrNm": "中華航空",   #航空公司
#     "Sn": 1
# }

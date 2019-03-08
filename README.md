# travel

## table schema
旅行社

* id: PK auto_increase
* 名稱: 


旅遊資訊 travel.csv
前面打* 是指至少抓取的欄位

* id: pk auto_increase
* 旅行社: FK(旅行社)
* 行程號: 跟 旅行社_id unique together 
* *旅遊天數
* *行程名稱
* *出發日期
* *價錢
* *可售位
* *總團位
* 星期
* 備註
* 報名狀態
* 是否保證出團
* 是否促銷
* 是否額滿
* 類型 
* 旅程連結
* 封面圖片連結

航班資訊 flight.csv
* id: pk auto_increase
* 旅遊資訊ID: FK(旅遊資訊)
* 旅行社: FK(旅行社) 
* 行程號: 跟 旅行社_id unique together 
* 天數
* 航班: FK(航空公司)
* 起飛日期
* 起飛時間
* 抵達日期
* 抵達時間
* RoutId
* 出發城市: FK(城市)
* 抵達城市: FK(城市)
* 出發地: FK(機場)
* 目的地: FK(機場)
* 航空公司: FK(航空公司)

## 檔案說明

* travelCrawler.py: 主程式
* requirements.txt: 程式環境
* travel.csv: 旅遊資訊資料 (目前是抓取1到5頁的資料)
* flight.csv: 航班資料

## travelCrawler.py 程式架構

執行方式
python travelCrawler.py 

參數
* 第一個參數是 抓第幾頁 default=1
* 第二個參數是 抓到幾頁 default=1

Ex. python travelCrawler.py 1 5

使用requests 抓取資料

寫了兩個旅行社的類別 OrangeTravel, NewamazingTravel

都繼承Base界面，定義要用的屬性及方法 可以爬取特定分頁 

屬性方法
* travelData: 旅遊資料
* flightData: 航班資料
* run(): 處理多分頁呼叫crawler()

OrangeTravel, NewamazingTravel 這兩個類別要去 特定網頁的爬蟲程式 crawler()

剛好這兩個網站程式差不多，故程式一樣

方法
* crawler(): 將結果加到 travelData
* filghtCrawler(): 將結果加到 flightData


MainApp 是做 資料存檔 這裡是使用csv 格式
去新建 OrangeTravel 與 NewamazingTravel, 並跑run()，都可以拿到travelData 和 flightData，分別寫csv檔案

### 擴充及維護性

如果要再爬另一間旅行社，寫一個 類別 繼承 Base 界面，寫這個網頁的爬蟲程式 回傳 旅行資訊資料

如果要換儲存格式可以在 MainApp 更改成 json 或 關聯式資料庫



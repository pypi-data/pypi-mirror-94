
import sys, os
import win32com.client

class CpUtil():
    def __request(self, endpoint):
        return win32com.client.Dispatch("CpUtil."+str(endpoint))
    
    # 연결 상태 확인
    def getConnected(self):
        """
        1 (connected), 0 (disconnected) 의 값을 boolean 으로 return
        """
        res = self.__request("CpCybos").isConnect
        if res == 1:
            is_connected = True
        else:
            is_connected = False

        return is_connected

    # 전체 종목 수
    def getStockCount(self):
        """
        전체 종목 갯수 int로 return
        """
        res = self.__request('CpStockCode').GetCount()
        return res

    # 전체 종목 코드 리스트
    def getStockCodeList(self):
        """
        전체 종목 코드 리스트 return
        """
        res = self.__request('CpCodeMgr').GetStockListByMarket(1)
        return res

    # 종목코드에 대한 종목 이름 반환
    def getStockCodeToName(self, stock_code):
        """
        stock_code 에 대한 종목 이름을 str으로 return
        """
        res = self.__request('CpCodeMgr').CodeToName(stock_code)
        return res

    # 전체 종목에 대한 코드 (key), 이름 (value) 반환
    def getStockCodeAndNameAll(self):
        """
        전체 종목에 대한 코드와 이름을 dict 로 return
        """

        stock_code_list = self.getStockCodeList()
        stock_info_obj = {}
        for stock_code in stock_code_list:
            stock_name = self.getStockCodeToName(stock_code)
            stock_info_obj[stock_code] = stock_name
        return stock_info_obj
    
    # 호출 제한까지 남은 호출량 확인
    def GetLimitRemainCount(self):
        """
        호출 제한까지 남은 호출량 확인
        """
        
        res = self.__request('CpCyBos').GetLimitRemainCount("LT_NONTRADE_REQUEST")
        return res

class CpSysDib():

    def getStockChartPriceToDate(self, date_count, stock_code):
        """
        stock_code 에 대한 chart return
        """
        date_list = []
        stock_last_price = []
        stock_high_price = []
        stock_low_price = []
        
        fields = [0, 3, 4, 5]

        inst_stock_chart = win32com.client.Dispatch("CpSysDib.StockChart")
        
        for field in fields:
            
            inst_stock_chart.SetInputValue(0, stock_code) #종목코드
            inst_stock_chart.SetInputValue(1, ord('2')) #1=기간, 2=갯수
            inst_stock_chart.SetInputValue(4, date_count) #요청 갯수
            #요청 받을 필드값
            inst_stock_chart.SetInputValue(5, field)
            #0: 날짜 / 1: 시간 / 2: 시가 / 3: 고가 / 4: 저가 / 5: 종가 / 8: 거래량 / 9: 거래대금
            inst_stock_chart.SetInputValue(6, ord('D')) #차트 구분
            # D: 일 / W: 주 / M: 월 / m: 분 / T: 틱
            inst_stock_chart.SetInputValue(9, ord('1'))
            inst_stock_chart.BlockRequest()

            data_count = inst_stock_chart.GetHeaderValue(3)
                
            if field == 0:
                for i in range(data_count):
                    year = str(inst_stock_chart.GetDataValue(0, i))[0:4]
                    month = str(inst_stock_chart.GetDataValue(0, i))[4:6]
                    day = str(inst_stock_chart.GetDataValue(0, i))[6:]
                    date = f'{year}-{month}-{day}'
                    date_list.append(date)
            elif field == 3:
                for i in range(data_count):
                    stock_high_price.append(inst_stock_chart.GetDataValue(0, i))
            elif field == 4:
                for i in range(data_count):
                    stock_low_price.append(inst_stock_chart.GetDataValue(0, i))
            elif field == 5:
                for i in range(data_count):
                    stock_last_price.append(inst_stock_chart.GetDataValue(0, i))

        return date_list, stock_high_price, stock_low_price, stock_last_price


    def getStockPer(self, stock_code):
        """
        stock_code 에 대한 PER 지수 반환
        """
        inst_market_eye = win32com.client.Dispatch("CpSysDib.StockUniMst")

        inst_market_eye.SetInputValue(0, stock_code)
        inst_market_eye.BlockRequest()

        per = inst_market_eye.GetHeaderValue(98)

        return per
    
class CpTrade():
    def __init__(self):
        self.cp_trade_util = win32com.client.Dispatch("CpTrade.CpTdUtil")
        self.cp_trade_util.TradeInit()
        self.account_number = self.cp_trade_util.AccountNumber[0]
        self.acc_flag = self.cp_trade_util.GoodsList(self.account_number, 1)
    
    def buyStock(self, stock_code):
        cp_trade = win32com.client.Dispatch("CpTrade.CpTd0311")
        
        cp_trade.SetInputValue(0, 2)    # 1: 매도, 2: 매수
        cp_trade.SetInputValue(1, self.account_number)  # 계좌번호
        cp_trade.SetInputValue(2, self.acc_flag[0])
        cp_trade.SetInputValue(3, stock_code)   # 종목 코드
        cp_trade.SetInputValue(4, 1)    # 주문수량
        cp_trade.SetInputValue(8, "03") # 3: 시장가, 12: 최유리, 13: 최우선
        
        cp_trade.BlockRequest()
        
        if not cp_trade.GetHeaderValue(8):
            return False
        
        return True
        
        
    def sellStock(self, stock_code):
        cp_trade = win32com.client.Dispatch("CpTrade.CpTd0311")
        
        cp_trade.SetInputValue(0, 1)    # 1: 매도, 2: 매수
        cp_trade.SetInputValue(1, self.account_number)  # 계좌번호
        cp_trade.SetInputValue(2, self.acc_flag[0])
        cp_trade.SetInputValue(3, stock_code)   # 종목 코드
        cp_trade.SetInputValue(4, 1)    # 주문수량
        cp_trade.SetInputValue(8, "03") # 03: 시장가, 12: 최유리, 13: 최우선
        
        cp_trade.BlockRequest()
        
        if not cp_trade.GetHeaderValue(8):
            return False
        
        return True
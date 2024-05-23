import FinanceDataReader as fdr
import OpenDartReader
import pandas as pd

class Dividend():
    def __init__(self, exchange="KRX"):
        self.exchange=exchange.upper()
    '''
    상장회사 가져오는 함수 GetStockList
    parameter로 self
    상장회사를 dataframe으로 return
    '''
    def GetStockList(self):
        # 상장회사 불러오기
        stock_list=fdr.StockListing(self.exchange)
        #KRX일 때 KONEX는 제외
        if self.exchange =="KRX":
            stock_list=stock_list.loc[stock_list["Market"]!="KONEX"]
        #상장회사 코드, 이름, 상장 거래소 가져오기
        stock_list=stock_list[['Code','Name','Market']]
        stock_list=stock_list.reset_index()
        stock_list.drop("index",axis=1,inplace=True)
        return stock_list
    
    '''
    특정 회사의 재무제표를 반환하는 함수 DisplayTable
    parameter로 self, api코드, 회사 코드, 연도
    특정 회사의 재무제표 dataframe으로 return
    '''
    def DispalyTable(self, api_code, code, year):
        #타입 변환
        code=str(code)
        year=int(year)
        #api 키 입력
        my_api=str(api_code)
        dart=OpenDartReader(my_api)
        #특정 회사 특정연도 재무제표 return
        return dart.report(code, "배당", year, "11011")
    
    '''
    배당률 탐색 함수 GetDividendRate
    parameter로 self, api코드, 연도, print_option은 True default
    배당률을 list로 return
    '''
    def GetDividendRate(self, api_code,year, print_option=1):
        # 상장회사 불러오기
        stock_list=self.GetStockList()
        length=len(stock_list) # 회사의 수
        stock_div_list=[] # 배당률 저장 리스트
        my_api=str(api_code)
        dart=OpenDartReader(my_api)
        for n in range(0, length):
            try:
                list1_append=False
                table=dart.report(stock_list["Code"][n],"배당",year,"11011")
                a=table.loc[list(table.loc[:,"se"]).index("현금배당수익률(%)"),"thstrm"]
                if print_option:
                    print(f"{n+1}/{length} fouded")
                if a=='-':
                    stock_div_list.append(0)
                    list1_append=True
                    if print_option:
                        print(f"{n+1}/{length} successed")
                else:
                    a=float(a)
                    stock_div_list.append(a)
                    list1_append=True
                    if print_option:
                        print(f"{n+1}/{length} successed")
            except:
                if not list1_append:
                    print(f"{n+1}/{length} failed")
                    if print_option:
                        stock_div_list.append(0)
        return stock_div_list

    '''
    주당 배당금을 가져오는 함수 GetDividendPerShare
    parameter로 self, api코드, 연도, pritn_option은 True로 default
    주당 배당금을 list로 return
    '''
    def GetDividendPerShare(self, api_code, year, print_option=1):
        stock_list=self.GetStockList()
        length=len(stock_list)
        stock_div_won=[] # 배당률 저장 리스트
        my_api=str(api_code)
        dart=OpenDartReader(my_api)
        for n in range(0,length):
            try:
                list2_append=False
                table=dart.report(stock_list["Code"][n],"배당",year,"11011")
                b=table.loc[list(table.loc[:,"se"]).index("주당 현금배당금(원)"),"thstrm"]
                if print_option:
                    print(f"{n+1}/{length} founded")
                if ',' in b:
                    b=float(b.replace(',',''))
                if b=='-':
                    stock_div_won.append(0)
                    list2_append=True
                    if print_option:
                        print(f"{n+1}/{length} successed")
                else:
                    stock_div_won.append(float(b))
                    list2_append=True
                    if print_option:
                        print(f"{n+1}/{length} seccessed")
            except:
                if not list2_append:
                    stock_div_won.append(0)
                    if print_option:
                        print(f"{n+1}/{length} failed")
        return stock_div_won
    
    '''
    배당률과 배당금을 가져오는 함수 GetDividendAll
    parameter로 self, api코드, 연도, print_option은 True default
    두 리스트를 dataframe으로 return
    '''
    def GetDividendAll(self, api_code, year, print_option=1):
        stock_list=self.GetStockList()
        length=len(stock_list)
        my_api=str(api_code)
        dart=OpenDartReader(my_api)
        stock_div_list=[] #당기
        stock_div_won=[] # 주당 현금배당금(원)
        for n in range(0,length):
            if len(stock_div_list)!=len(stock_div_won):
                print(n)
                break
            try:
                list1_appned=False
                list2_append=False
                table=dart.report(stock_list["Code"][n],"배당",year,"11011")
                a=table.loc[list(table.loc[:,"se"]).index("현금배당수익률(%)"),"thstrm"]
                if print_option:
                    print(f"{n+1}/{length} founded")
                if a=='-':
                    stock_div_list.append(0)
                    list1_appned=True
                else:
                    a=float(a)
                    stock_div_list.append(a)
                    list1_appned=True
                b=table.loc[list(table.loc[:,"se"]).index("주당 현금배당금(원)"),"thstrm"]
                if print_option:
                    print(f"{n+1}/{length} founded")
                if ',' in b:
                    b=float(b.replace(',',''))
                if b=='-':
                    stock_div_won.append(0)
                    list2_append=True
                    if print_option:
                        print(f"{n+1}/{length} seccussed")
                else:
                    stock_div_won.append(float(b))
                    list2_append=True
                    if print_option:
                        print(f"{n+1}/{length} successed")
                        

            except:
                if not list1_appned:
                    if print_option:
                        print(f"{n+1}/{length} failed")
                    stock_div_list.append(0)
                if not list2_append:
                    stock_div_won.append(0)
                    if print_option:
                        print(f"{n+1}/{length} failed")
        data_div=pd.DataFrame({"현금배당수익률(%)_당기":stock_div_list,
                       "주당 현금배당금(원)":stock_div_won})
        return data_div

    '''
    주식 목록과 data를 병합하는 함수 MergeWithStockList
    parameter로 self, data, axis_option과 sort_option은 default로 1
    병합한 dataframe을 return
    '''
    def MergeWithStockList(self, data, axis_option=1, sort_option=1):
        stock_list=self.GetStockList()
        data1=pd.concat([stock_list,data],axis=axis_option)
        if sort_option:
            data1.sort_values(by="현금배당수익률(%)_당기",ascending=False,inplace=True)
        return data1
    
    def SaveToCSV(self, data, path):
        data.to_csv(f"{path}.csv",encoding="euc-kr")

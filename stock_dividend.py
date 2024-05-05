import FinanceDataReader as fdr
import OpenDartReader
import pandas as pd
stock_list=fdr.StockListing("KRX")
stock_list=stock_list.loc[stock_list["Market"]!="KONEX"]

# stock_list는 회사코드, 이름, 상장거래소
stock_list=stock_list[['Code','Name','Market']]
stock_list=stock_list.reset_index()
stock_list.drop("index",axis=1,inplace=True)
length=len(stock_list["Name"]) #기업의 수

#api 키 입력
my_api="type your own api key"
dart=OpenDartReader(my_api)

stock_div_list=[] #당기배당률
stock_div_won=[] # 주당 현금배당금(원)

for n in range(0,length):
    #당기현금배당수익율
    if len(stock_div_list)!=len(stock_div_won):
        print(n)
        break
    try:
        list1_appned=False
        list2_append=False
        table=dart.report(stock_list["Code"][n],"배당",2023,"11011")
        a=table.loc[list(table.loc[:,"se"]).index("현금배당수익률(%)"),"thstrm"] #배당률 추출
        print(f"{n+1}/{length} 배당률 발견")
        if a=='-':
            a=0
            stock_div_list.append(a)
            list1_appned=True
        else:
            a=float(a)
            stock_div_list.append(a)
            list1_appned=True
        b=table.loc[list(table.loc[:,"se"]).index("주당 현금배당금(원)"),"thstrm"] #배당금 추출
        print(f"{n+1}/{length} 배당금 발견")
        if ',' in b:
            b=float(b.replace(',',''))
            print("b:str2float")
        if b=='-':
            stock_div_won.append(0)
            list2_append=True
        else:
            stock_div_won.append(float(b))
            list2_append=True
        print(f"{n+1}/{length} successful")
                

    except:
        if not list1_appned:
            print(f"{n+1}/{length} 배당률 발견실패")
            stock_div_list.append(0)
        if not list2_append:
            stock_div_won.append(0)
            print(f"{n+1}/{length} 배당금 발견실패")
        print(f"{n+1}/{length} not found")

#데이터 생성 및 병합
data_div=pd.DataFrame({"현금배당수익률(%)_당기":stock_div_list,
                       "주당 현금배당금(원)":stock_div_won})
data_fin=pd.concat([stock_list,data_div],axis=1)

data_fin.sort_values(by="현금배당수익률(%)_당기",ascending=False,inplace=True) #내림차순 정렬
#csv파일로 저장
data_fin.to_csv("배당금list_2023_배당률 배당금.csv",encoding="euc-kr")
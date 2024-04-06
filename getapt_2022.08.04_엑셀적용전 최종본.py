from genericpath import isfile
import requests
import json
import re
import sys
from bs4 import BeautifulSoup
import time as t
import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains


if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")

import pyautogui
import tkinter as tk
import logging
import datetime

d = datetime.datetime.now()
wrt_dt =d.strftime("%Y.%m.%d")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(u'%(asctime)s [%(levelname)8s] %(message)s')
# StreamHandler
streamingHandler = logging.StreamHandler()
streamingHandler.setFormatter(formatter)
# FileHandler
logfileNm = 'LOG_'+wrt_dt+'.log'
file_handler = logging.FileHandler(logfileNm)
file_handler.setFormatter(formatter)
# RotatingFileHandler
log_max_size = 10 * 1024 * 1024  ## 10MB
log_file_count = 20
logger.addHandler(file_handler)

icon_path = os.path.join(os.path.dirname(__file__), 'soonsuboy_profile.ico')
print (icon_path)


root = tk.Tk()
root.title("Get_apt_by_soonsuboy")
root.geometry("600x600")
if os.path.isfile(icon_path) :
    root.iconbitmap(icon_path)
    
label1 = tk.Label(root,  text="지역 입력하세요 \n ex)강남구 삼성동")
label2 = tk.Label(root,  text="조회할 세대수 입력 \n ex)300 -> 300이상조회")
inputregion = tk.Entry(root, width=15, font=("Courier",8), borderwidth=5)
inputregion.insert(0,'')
inputsaedae = tk.Entry(root, width=15, font=("Courier",8), borderwidth=5)
inputsaedae.insert(0,'200')
label1.grid(column=0, row=0 , padx=5, pady=5 )
label2.grid(column=1, row=0 , padx=5, pady=5 )
inputregion.grid(column=0, row=1 , padx=5, pady=5)
inputsaedae.grid(column=1, row=1 , padx=5, pady=5)

tkpyung=tk.StringVar()
saedae=tk.StringVar()
Rpyung28    = tk.Radiobutton(root , text='23~27평', value = 1  ,variable=tkpyung )
Rpyung2931  = tk.Radiobutton(root , text='28~31평(낀평)', value =2 ,variable=tkpyung )
Rpyung32    = tk.Radiobutton(root , text='32평 이상', value = 3 ,variable=tkpyung )

Rpyung28.grid(column=3, row=0)
Rpyung2931.grid(column=3, row=1)
Rpyung32.grid(column=3, row=2)
Rpyung32.select()

btn7 = tk.Button(root, text='시작', padx=10, pady=5, font=("Courier",10),command=lambda: button_clicked(inputregion,tkpyung,inputsaedae))
btn7.grid(column=1, row=3)

btn8 = tk.Button(root, text='닫기', padx=10, pady=5, font=("Courier",10),command=lambda: button_clolse_clicked())
btn8.grid(column=1, row=4)
## 평대#23~27평#28~31평#31평 이상#범위입력

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


wall = tk.PhotoImage(file = "soonsuboy_profile.png")
wall_label = tk.Label(image = wall) 
wall_label.grid(column=1, row=5)
labelbottom = tk.Label(root,  text="※평형 조건이 맞지 않는 단지는 최소평수 최저가격 조회됩니다\n※입력한 지역근처 이외의 단지가 나올 수 있습니다")
labelbottom.grid(column=1, row=6 , padx=5, pady=5 )
labelbottom = tk.Label(root,  font=("Courier",8), text="아파트 정보/가격 자동화 for 월부 by 순수보이")
labelbottom.grid(column=1, row=7 , padx=5, pady=5 )


city =''

def button_clolse_clicked():
    sys.exit(1)
    

def floorChek (spec):
    for index, value in enumerate(spec):
        realFloor = ''
        totalFloor=''
        print(index , value.text.replace(',','').split())
        parsfloor=value.text.replace(',','').replace('층','').split()
        # print (len(parsfloor[1])) # 3 : 4/6 ,4: 1/23 ,5 :12/44
        if int(len(parsfloor[1])) ==3 :
            realFloor =parsfloor[1][0:1]
            totalFloor=parsfloor[1][2:3]
            print('3 realFloor/totalFloor' ,realFloor,totalFloor)
            logger.info('3 realFloor/totalFloor %s , %s' ,realFloor,totalFloor)
            if realFloor==totalFloor :
                realFloor='top'
                print('top realFloor/totalFloor' ,realFloor,totalFloor)
                logger.info('top realFloor/totalFloor %s , %s' ,realFloor,totalFloor)
        elif int(len(parsfloor[1])) ==4 :
            realFloor =parsfloor[1][0:1]
            totalFloor=parsfloor[1][2:4]
            print('4 realFloor/totalFloor' ,realFloor,totalFloor)
            logger.info('4 realFloor/totalFloor %s , %s' ,realFloor,totalFloor)
            if realFloor==totalFloor :
                realFloor='top'
                print('4 realFloor/totalFloor' ,realFloor,totalFloor)
                logger.info('4 realFloor/totalFloor %s , %s' ,realFloor,totalFloor)
        elif int(len(parsfloor[1])) ==5 :
            realFloor =parsfloor[1][0:2]
            totalFloor=parsfloor[1][3:5]
            print('5 realFloor/totalFloor' ,realFloor,totalFloor)
            logger.info('5 realFloor/totalFloor %s , %s' ,realFloor,totalFloor)
            if realFloor==totalFloor :
                realFloor='top'
                print('5 realFloor/totalFloor' ,realFloor,totalFloor)
                logger.info('5 realFloor/totalFloor %s , %s' ,realFloor,totalFloor)
        else :
            break

    return realFloor 

def pyungChek (spec): # 5: 87/65 , 6:114/84 , 7:120/101
    for index, value in enumerate(spec):
        Gpyung = '0'
        Jpyung = '0'                  
        parspyung=value.text.replace(',','').replace('층','').replace('A','').replace('B','').replace('C','').replace('m²','').split()        
        print('parspyung' , parspyung)
        print (len(parspyung[0]), parspyung[0])
        if int(len(parspyung[0])) ==5 :
            Gpyung =str(int(int(parspyung[0][0:2])/3.3))
            Jpyung =str(int(int(parspyung[0][3:5])/3.3))
            print('5 Gpyung/Jpyung' ,Gpyung,Jpyung)            
            logger.info('5 Gpyung/Jpyung %s , %s' ,Gpyung,Jpyung)      
        elif int(len(parspyung[0])) ==6 :
            Gpyung =str(int(int(parspyung[0][0:3])/3.3))
            Jpyung =str(int(int(parspyung[0][4:6])/3.3))
            print('6 Gpyung/Jpyung' ,Gpyung,Jpyung)            
            logger.info('6 Gpyung/Jpyung %s , %s' ,Gpyung,Jpyung)      
        elif int(len(parspyung[0])) ==7 :
            Gpyung =str(int(int(parspyung[0][0:3])/3.3))
            Jpyung =str(int(int(parspyung[0][5:7])/3.3))
            print('7 Gpyung/Jpyung' ,Gpyung,Jpyung)
            logger.info('7 Gpyung/Jpyung %s , %s' ,Gpyung,Jpyung)      
        elif int(len(parspyung[0])) >7 :
            Gpyung =str(int(int(parspyung[0][0:3])/3.3))            
            print('>7 Gpyung/Jpyung' ,Gpyung,Jpyung)    
            logger.info('>7 Gpyung/Jpyung %s , %s' ,Gpyung,Jpyung)      
        else :
            break          
    
    return Gpyung 

def wayChek (spec): 
    for index, value in enumerate(spec):
        way = ''             
        parsway=value.text.replace(',','').replace('층','').replace('m²','').split()                
        way = parsway[2]        
                
    return way 

def pasprice (p_price): 
    r_price =''
    p_price= p_price.replace(' ','')
    if p_price.find(',') !=-1 :                
        print('pasprice     1' ,p_price , p_price.find(','))
        logger.info('pasprice     1 %s , %s' ,p_price , p_price.find(','))
        r_price= p_price.replace(',','').replace('억','').replace(' ','')
    elif p_price.find(',') == -1 :
        print('pasprice    2' ,p_price ,len(p_price))
        logger.info('pasprice     2 %s , %s' ,p_price ,len(p_price))
        if len(p_price) ==2: #1억            
            r_price= p_price.replace(',','').replace('억','0000').replace(' ','')
            print('pasprice    3' ,r_price)
            logger.info('pasprice     3 %s  ' ,r_price )
        elif len(p_price) ==3: #10억            
            r_price= p_price.replace(',' , '').replace('억','0000').replace(' ','')
            print('pasprice   4' ,r_price)
            logger.info('pasprice     4 %s  ' ,r_price )
        else : #1억500            
            r_price= p_price.replace(',','').replace('억','0').replace(' ','')
            print('pasprice   5' ,r_price)      
            logger.info('pasprice     5 %s  ' ,r_price )
                
    return r_price 





pyungstart=''
pyungend=''
inserted_pyung =''
MJprice0 ='0'
uploadnum=-1
price_list={}
upolad_list =[]
        
def button_clicked(region,tkpyung, tksaedae):      
    
    if region.get() =='' :
        pyautogui.alert ("지역을 입력해주세요")
        return
    
    if tksaedae.get() =='' :
        pyautogui.alert ("세대수를 입력해주세요")
        return
    
    
    if tkpyung.get() == '1' :        
        pyungstart = "76"
        pyungend = "89.3"
    elif tkpyung.get() == '2' :        
        pyungstart = "92.6"
        pyungend = "102.5"
    elif tkpyung.get() == '3' :        
        pyungstart = "105.8"
        pyungend = "132.2"
        
    print(region.get() , pyungstart , ' ~ ', pyungend)  
    city =region.get()    
    v_saedae    =tksaedae.get()
    # city ="강남구 역삼동"
    # city ="천안시 두정동"

    URL = "https://m.land.naver.com/search/result/" + city
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"}
    res= requests.get(URL ,headers=headers)
    print(URL)
    res.raise_for_status()
    print("응답코드 : ", res.raise_for_status())

    soup = BeautifulSoup(res.text, "lxml")
    # soup.selet("script")

    print(soup.title.get_text())
    print(soup.script.attrs)

    # <script src="https://ssl.pstatic.net/tveta/libs/glad/prod/gfp-core.js"></script>

    # print(soup.find_all('script'))
    print("soup.find_all('script')" , type(soup.find_all('script')))

    data_script = soup.find_all('script')

    #print( data_script[3].text , 'sdw type+2:   ', type(data_script[3].text) )
    # "filter:\" ~"/},"
    # filter 가 포함된 자바스크립트 추출
    data_string =data_script[3].text

    # filter 부분 데이터 추출 
    data_string = data_string.split("filter:")[-1].split("},")[0]
    print( data_string , 'sdw type+1:   ', type(data_string) )

    data_string = data_string.replace('{','').replace('}','').replace(' ','').replace('\n','').replace('"','').replace("'",'').split(',')

    print( data_string , 'sdw type+3:   ', type(data_string) )

    print( 'lat:' ,data_string[0].replace('lat:',''))
    print( 'lon:' ,data_string[1].replace('lon:',''))
    print( 'z:' ,data_string[2].replace('z:',''))
    print( 'cortarNo:' ,data_string[3].replace('cortarNo:',''))
    v1_lat      = data_string[0].replace('lat:','')
    v1_lon      = data_string[1].replace('lon:','')
    v1_z        = data_string[2].replace('z:','')
    v1_cortarNo = data_string[3].replace('cortarNo:','')

    step1Url ='https://m.land.naver.com/cluster/clusterList?cortarNo='+v1_cortarNo+'&rletTpCd=APT&tradTpCd=A1%B1%B2&z='+v1_z+'&lat='+v1_lat+'&lon='+v1_lon+'&pCortarNo=&addon=COMPLEX'
    print( 'step1Url:' ,step1Url)

    cluster1 = requests.get(step1Url ,headers=headers)
    #print(cluster1.text)
    cluster1_parsed = cluster1.text
    cluster1_parsed = cluster1_parsed.split('{"code":"success","data":{"COMPLEX":[')[-1].split(']},')[0]
    cluster1_parsed_lgeo = cluster1_parsed.split('"lgeo":')

    apt_no=[]
    apt_saedae_check=[]

    for index2, value2 in enumerate(cluster1_parsed_lgeo) :
        # print("---------------------------------",index2 , value2[1:11] , "sdw type+", type(value2))           
        final_url ='https://m.land.naver.com/cluster/ajax/complexList?itemId='+value2[1:11]+'&mapKey=&lgeo='+value2[1:11]+'&rletTpCd=APT&tradTpCd=A1%B1%B2&z='+v1_z+'&lat='+v1_lat+'&lon='+v1_lon
        # https://m.land.naver.com/cluster/ajax/complexList?itemId='+value2[1:12]+'&mapKey=&lgeo='+value2[1:12]+'&rletTpCd=APT&tradTpCd=A1%B1%B2&z='+v1_z+'&lat='+v1_lat+'&lon=+v1_lon
        print(final_url)
        cluster2 = requests.get(final_url ,headers=headers)
        cluster2_parsed = cluster2.text
        cluster2_parsed = cluster2_parsed.split('{"result":[{')[-1].split('],"more"')[0]
        cluster2_parsed_hscpNo = cluster2_parsed.split('"hscpNo":')

        for index3, value3 in enumerate(cluster2_parsed_hscpNo) :
            apt_no_check ='x'
            apt_saedae_check='x'
            # print(index3 , value3.split('","hscpNm"')[0].replace('"','') , "sdw type+", type(value2))
            apt_no_check = value3.split('","hscpNm"')[0].replace('"','')            
            apt_saedae_check = value3.split('"totHsehCnt":')[-1].split(',"genHsehCnt"')[0]
            if apt_saedae_check !='' and apt_saedae_check != '{"more":false}':
                
                if int(apt_saedae_check)>int(v_saedae) :
                    print('2' , apt_saedae_check)
                    if apt_no_check !='' and apt_no_check !='{more:false}':
                        print('3' , apt_saedae_check)
                        apt_no.append(apt_no_check)         
        
#        cluster2_parsed_saedae = cluster2_parsed.split('"totHsehCnt":')
#        for index33, value33 in enumerate(cluster2_parsed_saedae) :
#            apt_saedae_check ='x'
#            apt_saedae_check = value33.split(',"genHsehCnt"')[0]
#            if apt_saedae_check !='' and apt_saedae_check !='{more:false}':
#                apt_saedae_check.append(apt_saedae_check)
            




    driver = webdriver.Chrome()
    URL_APT_NO = "https://new.land.naver.com/complexes/"
    
    # url = 'https://new.land.naver.com/complexes/8621?&a=:JGC:ABYG:APT&b=B1:A1&h=66&i=132'
   

    def get_naver_complex(datacount,id):
        driver.get(URL_APT_NO + str(id) + "?&a=:JGC:ABYG:APT&b=B1:A1&h="+pyungstart+"&i="+pyungend+"&ad=true")
        apt_region=''        
        atp_nm =''
        data = []
        try:
            # if datacount==0 :
            #     data.append('아파트번호')
            #     data.append('부동산 타입')
            #     data.append('시')
            #     data.append('구')
            #     data.append('동')
            #     data.append('아파트명')
            #     data.append('세대수')
            #     data.append('동갯수')
            #     data.append('아파트연식')
            #     data.append('평형정보')
            #     data.append('매물평형')
            #     data.append('매물층')
            #     data.append('전세가')
            #     data.append('전세가')
            #     data.append('매매가')
            #     data.append('매매가')
                
                
            data.append(id)
            category = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "label--category"))).text
            data.append(category)
            
            time.sleep(1)
            index = 1
            for region in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "is-selected"))):
                data.append(region.text)
                if index == 3:
                    apt_region = region.text
                    break
                index = index + 1          
          
            title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "complexTitle"))).text
            data.append(title)
            atp_nm = apt_region + ' ' +title

            for feature in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#summaryInfo > .complex_feature > dd"))):                
                feature =feature.text.replace('㎡','').split('\n')
                data.append(feature[0])                
            
            
            
            
            
            #없는 아파트 검색해서 결과 없을때
            try :
                elem1 = WebDriverWait(driver , 0.5).until(EC.presence_of_element_located ((By.XPATH,"//*[@id='ct']/div[2]/div[2]/div[1]/div/h3" )))
                print('-------------------------------검색 NO DATA----------------------------------------------' )
                # upolad_list.append([title ,'x', 'x','x' ,'x'] )
                logger.info("no result apt : %s",id)                         
            except :
                datacount +=1
                print('-------------------------------',datacount,atp_nm,'검색 OK----------------------------------------------' )    
                logger.info('-------------------------------검색 OK %s, %s',datacount,atp_nm)    
        
            try :
                driver.find_element(By.XPATH,"//*[@id='complexOverviewList']/div[2]/div[1]/div[3]/a[3]").click()
                # 정렬한 아파트 가격이 나올때가지 기다린다.
                elem = WebDriverWait(driver , 3).until(EC.presence_of_element_located ((By.XPATH,"//*[@id='articleListArea']" )))        
                # 스크롤링으로 전체 데이터 가져온다.        
                driver.execute_script("document.querySelector('#complexOverviewList > div > div.item_area > div').scrollTop = document.querySelector('#complexOverviewList > div > div.item_area > div').scrollHeight;")
                # driver.execute_script("document.querySelector('.item_list--article').scrollTop = 0;")
                
                time.sleep(0.5)        
                v_datachek = 0 #전세 매매 가격 추출 여부 
                global uploadnum 
                # 위에가 전센지 매매인지 확인한다. 데이터는 1부터 시작
                for datanum in range(1,4000) :
                    driver.execute_script("document.querySelector('#complexOverviewList > div > div.item_area > div').scrollTop = document.querySelector('#complexOverviewList > div > div.item_area > div').scrollHeight;")
                    j_Or_m=''
                    MJprice=''
                    spec=[]
                    parsfloor=[]
                    try :
                        #단지내 물건 순서 1번이 낮은가격순
                        dataelem = WebDriverWait(driver , 2).until(EC.presence_of_element_located ((By.XPATH,"//*[@id='articleListArea']/div["+str(datanum)+"]/div[1]/a/div[2]/span[1]" )))
                        #단지내 물건 상세 정보
                        price_list = driver.find_element(By.XPATH,"//*[@id='articleListArea']/div["+str(datanum)+"]/div").text
                        #단지내 물건 전세, 매매 여부확인
                        j_Or_m =driver.find_element(By.XPATH,"//*[@id='articleListArea']/div["+str(datanum)+"]/div[1]/a/div[2]/span[1]").text   
                        MJprice=driver.find_element(By.XPATH,"//*[@id='articleListArea']/div["+str(datanum)+"]/div/a/div[2]/span[2]").text                
                        spec = driver.find_elements(By.XPATH,"//*[@id='articleListArea']/div["+str(datanum)+"]/div[1]/a/div[3]/p[1]/span[1]")
                                                
                        if j_Or_m =='전세' and v_datachek ==0 :
                            #전세 층수 뽑아내기--------------------------------------------------------                    
                            realFloor = floorChek(spec)
                            Gpyung = pyungChek(spec)
                            way = wayChek(spec)
                            MJprice= pasprice(MJprice)
                            if realFloor != '1' and realFloor != '2' and realFloor != '3' and realFloor != '4' and realFloor != '저'and realFloor != 'top' : 
                                #평형, 층, 향, 전세가격 추출                        
                                print(datanum , '기준전세입력--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice:',atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )
                                logger.info(' %s , 기준전세입력--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice: %s ,%s,%s,%s,%s,%s', datanum ,atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )                                
                                data.append(Gpyung)
                                data.append(realFloor)
                                data.append('전세가')
                                data.append(MJprice)                               
                                inserted_pyung=Gpyung                               
                                uploadnum +=1                               
                                v_datachek =1                               
                            else : # 기준 층 없으면 그냥 최소가격 하나 뽑아내자                        
                                print(datanum , '최저전세입력--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice:',atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )
                                logger.info(' %s , 최저전세입력--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice: %s ,%s,%s,%s,%s,%s', datanum ,atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )                                
                                data.append(Gpyung)
                                data.append(realFloor)
                                data.append('전세가')
                                data.append(MJprice)                  
                                inserted_pyung=Gpyung 
                                uploadnum +=1
                                v_datachek =1
                        elif j_Or_m =='매매'  and v_datachek ==1 :
                            #매매 층수 뽑아내기--------------------------------------------------------   
                            realFloor = floorChek(spec)
                            Gpyung = pyungChek(spec)
                            way = wayChek(spec)
                            MJprice= pasprice(MJprice)
                            if inserted_pyung == Gpyung:
                                print(datanum , '전세입력후 매매입력--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice:',atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )
                                logger.info(' %s , 전세입력후 매매입력--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice: %s ,%s,%s,%s,%s,%s', datanum ,atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )                                
                                v_datachek =2
                                data.append('매매가')
                                data.append(MJprice)
                                break      
                                                    
                        elif j_Or_m =='매매'  and v_datachek ==0 : #매매밖에 없다면
                            #매매 층수 뽑아내기--------------------------------------------------------   
                            realFloor = floorChek(spec)
                            Gpyung = pyungChek(spec)
                            way = wayChek(spec)
                            MJprice= pasprice(MJprice)                            
                            print(datanum , '매매만--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice:',atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )
                            logger.info(' %s , 매매만--------- atp_nm j_Or_m , realFloor  ,Gpyung ,way,MJprice: %s ,%s,%s,%s,%s,%s', datanum ,atp_nm , j_Or_m ,realFloor,Gpyung,way,MJprice )
                            data.append(Gpyung)
                            data.append(realFloor)
                            data.append('전세가')
                            data.append(MJprice0)
                            data.append('매매가')
                            data.append(MJprice)
                            uploadnum +=1
                            v_datachek =2    
                            break                    
                        
                    except Exception as e:
                        print("[exception] 발생 : {}".format(e))
                        print('3.0 여기로 오면 에러 또는 완료' )
                        logger.info('3.0 여기로 오면 에러 또는 완료' )
                        break                    
            except :
                print('-------------------------------스크롤 NO DATA----------------------------------------------' )
                # upolad_list.append([atp_nm ,'0', '0','0' ,'0'] )
        
        
        
        

            

        except (NoSuchElementException, TimeoutException) as e:
            print(e)
            return -1

        with open('Result_apt_tracking_by_soonsuboy.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(data)

        return 1

                
                
    failed_id = []
    for i, v in enumerate(apt_no) :
        print(i, v )
        if get_naver_complex(i,v) < 0:
            failed_id.append(v)    
        
        # if i == 6:
        #     break;
        
            
    print(failed_id)

    driver.quit()
root.mainloop()
#https://new.land.naver.com/complexes/ + apt_no

# pyinstaller  -w -F  -i="soonsuboy_profile.ico" --add-data="soonsuboy_profile.ico;."  --add-data "soonsuboy_profile.png;." getapt.py
# pyinstaller  -w -F   getapt.py

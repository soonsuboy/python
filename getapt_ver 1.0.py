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
import tkinter as tk

root = tk.Tk()
root.title("Get_apt_by_soonsuboy")
root.geometry("400x500")

label1 = tk.Label(root,  text="지역 입력하세요 ex)강남구 삼성동")
pyungstart = tk.Entry(root, width=50, font=("Courier",8), borderwidth=5)
pyungstart.insert(0,'')
label1.grid(column=1, row=0 , padx=5, pady=5 )
pyungstart.grid(column=1, row=1 , padx=5, pady=5)
btn7 = tk.Button(root, text='시작', padx=10, pady=5, font=("Courier",10),command=lambda: button_clicked(pyungstart))
btn7.grid(column=1, row=3)

btn8 = tk.Button(root, text='닫기', padx=10, pady=5, font=("Courier",10),command=lambda: button_clolse_clicked())
btn8.grid(column=1, row=4)

wall = tk.PhotoImage(file = "soonsuboy_profile.png")
wall_label = tk.Label(image = wall) 
wall_label.grid(column=1, row=5)


city =''

def button_clolse_clicked():
    sys.exit(1)
    
    
def button_clicked(pyung):      
    print(pyung.get())  
    city =pyung.get()




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

    for index2, value2 in enumerate(cluster1_parsed_lgeo) :
        print("---------------------------------",index2 , value2[1:11] , "sdw type+", type(value2))           
        final_url ='https://m.land.naver.com/cluster/ajax/complexList?itemId='+value2[1:11]+'&mapKey=&lgeo='+value2[1:11]+'&rletTpCd=APT&tradTpCd=A1%B1%B2&z='+v1_z+'&lat='+v1_lat+'&lon='+v1_lon
        # https://m.land.naver.com/cluster/ajax/complexList?itemId='+value2[1:12]+'&mapKey=&lgeo='+value2[1:12]+'&rletTpCd=APT&tradTpCd=A1%B1%B2&z='+v1_z+'&lat='+v1_lat+'&lon=+v1_lon
        print(final_url)
        cluster2 = requests.get(final_url ,headers=headers)
        cluster2_parsed = cluster2.text
        cluster2_parsed = cluster2_parsed.split('{"result":[{')[-1].split('],"more"')[0]
        cluster2_parsed_hscpNo = cluster2_parsed.split('"hscpNo":')

        for index3, value3 in enumerate(cluster2_parsed_hscpNo) :
            apt_no_check ='x'
            print(index3 , value3.split('","hscpNm"')[0].replace('"','') , "sdw type+", type(value2))
            apt_no_check = value3.split('","hscpNm"')[0].replace('"','')
            if apt_no_check !='' and apt_no_check !='{more:false}':
                apt_no.append(apt_no_check)         




    driver = webdriver.Chrome()
    URL_APT_NO = "https://new.land.naver.com/complexes/"


    def get_naver_complex(id):
        driver.get(URL_APT_NO + str(id))

        data = []
        try:
            data.append(id)
            category = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "label--category"))).text
            data.append(category)
            
            time.sleep(1)
            index = 1
            for region in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "is-selected"))):
                data.append(region.text)
                if index == 3:
                    break
                index = index + 1
          
          
            title = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "complexTitle"))).text
            data.append(title)

            for feature in WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#summaryInfo > .complex_feature > dd"))):                
                feature =feature.text.replace('㎡','').split('\n')
                data.append(feature[0])                
                

            

        except (NoSuchElementException, TimeoutException) as e:
            print(e)
            return -1

        with open('Result_apt_by_soonsuboy.csv', 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',',quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(data)

        return 1

                
                
    failed_id = []
    for i, v in enumerate(apt_no) :
        print(i, v )
        if get_naver_complex(v) < 0:
            failed_id.append(v)    
        
        # if i == 3:
        #    break;
        
            
    print(failed_id)

    driver.quit()
root.mainloop()
#https://new.land.naver.com/complexes/ + apt_no

# pyinstaller -w -F getapt.py

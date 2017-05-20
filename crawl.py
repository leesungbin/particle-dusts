import requests
from bs4 import BeautifulSoup

from math import *

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def spider(y,m,o): #year,month,day
    year=y
    month=m
    obs=o #1 11 21
    #starting year,month,day have to be set
    #datas that will be returned
    hr_data=[]
    pm10_data=[]
    #pm25_data=[]
    liter_data=[]
    nope=0
    notadequate=0
    adequate=0
    while 1:
        data_matrix=[[0 for col in range(14)] for row in range(25)]
        col=0
        row=0
        
        if year==2017 and month ==5 and obs==21:
            print "missing data : " + str(nope)
            print "not adequate : " + str(notadequate)
            print "adequate : " + str(adequate)
            break
        url='http://www.kma.go.kr/weather/climate/past_tendays.jsp?stn=108&yy='+str(year)+'&mm='+str(month)+'&obs='+str(obs)
        source_code = requests.get(url)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'lxml')
        for td in soup.select('tbody > tr'):
            if col==16 or col==18:
                col+=1
                continue
            elif col>=25:
                break
            else:
                for tds in td.select('td'):
                    if str(tds.string) =='-' or str(tds.string) == '\xc2\xa0':
                        temp='0'
                    else:
                        temp=str(tds.string)
                    data_matrix[col][row]=float(temp)
                    row+=1
                col+=1
                row=0
                
        #data_matrix[24] checking is needed
        t=month_type(year,month,obs)
        if t==1:
            r=10
        elif t==2:
            r=11
        elif t==3:
            r=8
        else:
            r=9
            
        for i in range(0,r):
            if data_matrix[24][i]>=20 : #hour check
                
                
                pyear,pmonth,pobs=pymo1(year,month,obs,i)
                special_url1='http://openapi.seoul.go.kr:8088/556d7274556c736234364f4b464255/xml/DailyAverageAirQuality/1/5/'+str(pyear)+str(pmonth)+str(pobs)+'/%EB%8F%99%EB%8C%80%EB%AC%B8%EA%B5%AC/'
                print "checking "+pyear+pmonth+pobs
                dates=pyear+pmonth+pobs
                if year==2011 and month==5 and obs+i==31 or year==2011 and month==5 and obs+i==9 or year==2011 and month==5 and obs+i==20:
                    print "nodata"
                    nope+=1
                    break
                
                pyear,pmonth,pobs=pymo2(year,month,obs,i)
                special_url2='http://openapi.seoul.go.kr:8088/556d7274556c736234364f4b464255/xml/DailyAverageAirQuality/1/5/'+str(pyear)+str(pmonth)+str(pobs)+'/%EB%8F%99%EB%8C%80%EB%AC%B8%EA%B5%AC/'
                
                #print pyear,pmonth,pobs
                                                         
                source_code1=requests.get(special_url1)
                plain_text1=source_code1.text
                soup1=BeautifulSoup(plain_text1,'lxml')
                
                
                source_code2=requests.get(special_url2)
                plain_text2=source_code2.text
                soup2=BeautifulSoup(plain_text2,'lxml')
                
                
                tempm1=str(soup1.select('pm10')[0].string)
                tempm2=str(soup2.select('pm10')[0].string)
                #tempm3=str(soup1.select('pm25')[0].string)
                #tempm4=str(soup2.select('pm25')[0].string)
                    
                if tempm1 == 'None' or tempm2=='None' :
                    print "nope - now"
                    nope+=1
                    break
                #elif tempm3=='None' or tempm4=='None':
                 #   print "nope - yesterday"
                  #  nope+=1
                   # break
                else:
                    delta1=float(tempm1)-float(tempm2)
                    if delta1<0:
                        pm10_data.append([float(tempm2),delta1])
                        #delta2=float(tempm3)-float(tempm4)
                        #pm25_data.append([float(tempm3),delta2])
                        hr_data.append([dates,data_matrix[24][i]])
                        liter_data.append(data_matrix[22][i])
                        print "created data"
                        adequate+=1
                    else :
                        print "not adequate"    
                        notadequate+=1
        
        obs+=10
        year,month,obs=sugo(year,month,obs)
        
        
    return (hr_data,pm10_data,liter_data)#,pm25_data)
def pymo1(y,m,o,i):
    year=y
    month=m
    obs=o
    
    if m<10:
        month='0'+str(month)
        year=str(year)
        if o+i<10:
            obs='0'+str(o+i)
        else:
            obs=str(o+i)
    else:
        month=str(month)
        year=str(year)
        if o+i<10:
            obs='0'+str(o+i)
        else:
            obs=str(o+i)
    return (year,month,obs)

def pymo2(y,m,o,i): #go to yesterday
    year=y
    month=m
    obs=o
    
    if o+i-1>0:
        if m<10:
            if obs+i-1<10:
                return (str(year),'0'+str(month),'0'+str(obs+i-1))
            else:
                return (str(year),'0'+str(month),str(obs+i-1))
        else:
            if obs+i-1<10:
                return (str(year),str(month),'0'+str(obs+i-1))
            else:
                return (str(year),str(month),str(obs+i-1))     
    else:
        if m-1>0: #except 1
            if m-1 in [4,6,9,11]:
                if m-1==11:
                    return (str(y),str(m-1),'30')
                else:
                    return (str(y),'0'+str(m-1),'30')
            elif m-1!=2:
                if m-1 in [10,12]:
                    return (str(y),str(m-1),'31')
                else:
                    return (str(y),'0'+str(m-1),'31')
            else:
                if y % 4 ==0 and y % 100 != 0  or y %400==0:
                    return (str(y),'02','29')
                else:
                    return (str(y),'02','28')
        else: #if m==1
            return (str(y-1),'12','31')

def sugo(y,m,o):
    year=y
    month=m
    obs=o
    if obs==31:
        obs=1
        month+=1
        if month==13:
            month=1
            year+=1
    return (year,month,obs)

def month_type(y,m,o):
    if m in [4,6,9,11]:
        return 1
    elif m in [1,3,5,7,8,10,12] and o==21:
        return 2
    elif m in [1,3,5,7,8,10,12]:
        return 1
    elif m ==2 and o!=21:
        return 1
    else:
        if y % 4 ==0 and y % 100 != 0  or y %400==0:
            return 4
        else:
            return 3
        




hr,pm10,power=spider(2003,4,11) #,,pm25

f=open("over20.txt","w")
f.write("date"+" "+"hr"+ " "+ "pm10" + " " + "delta" + " " + "power")
for i in range(0,len(hr)):
    power[i]=power[i]/hr[i][1]
    f.write(str(hr[i][0])+" "+str(hr[i][1])+" "+str(pm10[i][0])+" "+str(pm10[i][1])+" "+str(power[i])+"\n")
f.close()

#def calc():
#    t90=[]
#    a=[]
#    b=[]
#    k=[]
#    h=2000;
#    rho_w=1000;
#    rho_a=((-0.0977*2+1.225)+1.225)/2;
#    Cd=0.47;
#    g=9.80;
#    for i in range(0,len(hr)):
#        x=power[i]
#        if x<=0.4:
#            r=1.24/2/1000
#            v=5.53
#            Nr=280
#        elif x<=1.5 :
#            r=1.60/2/1000
#            v=6.28
#            Nr=495
#        elif x<=6.0:
#            r=2.05/2/1000
#            v=7.11
#            Nr=495
#        elif x<=16.0:
#            r=2.40/2/1000
#            v=7.69
#            Nr=818
#        else:
#            r=2.85/2/1000
#            v=8.38
#            Nr=1220
#              
#        Nr_m3=Nr/v
#        V=4/3*pi*r**3
#        Vpath=pi*r**2*h
#        mass=V*rho_w
#        A=pi*r**2
#        v=sqrt(mass*g/(1/2*rho_a*Cd*A))
#        tf=h/v
#        
#        b.append(log(pm10[i][0]+pm10[i][1][i]))/pm10[i][0]/(-1*hr[i][1]*3600)
#        a.append(pm10[i][0])
#        k.append(b[i]*hr[i][1]*3600/(Nr_m3*Vpath/tf))
#        t90.append(log(0.1)/-b[i]/3600/24)
#    
#    average=sum(t90)/len(t90)
#    print average
#    print max(t90)
#    print min(t90)
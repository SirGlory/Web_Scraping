# Please note code scraps ~250 pages, this may take 6-10 minuites to run  
    
# Imports
import requests
from bs4 import BeautifulSoup
import time
import pandas

# Create Variables
t0 = time.time()
r=requests.get("https://www.property24.com/apartments-to-rent/cape-town/western-cape/432", 
               headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content
soup=BeautifulSoup(c,"html.parser")
all=soup.find_all("span",{"class":"p24_content"})
l=[]
base_url= "https://www.property24.com/apartments-to-rent/cape-town/western-cape/432"


# For Loop running through each page and pulling content
for page in range(1,246,1):
    print(base_url+"/p"+str(page))
    r=requests.get(base_url+"/p"+str(page))
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("span",{"class":"p24_content"})
    
# For Loop drawing each attribute from specific HTML division
    for item in all :
        d={}
        d["Price"]=item.find("span",{"class":"p24_price"}).text.replace("\n","").replace(" ","").replace("\r","")
        d["Locate"]=item.find_all("span",{"class","p24_location"})[0].text

        try:
            d["Address"]=item.find_all("span",{"class","p24_address"})[0].text
        except:
            d["Address"]=None

        try:
            d["Beds"]=item.find("span",{"class","p24_featureDetails","title","Bedrooms"}).text.replace("\n","")
        except:
            d["Beds"]=None

        l.append(d)
        
# Timing of code        
t1 = time.time()
total = round(t1-t0,3)
totalm = round(total/60,3)
print(" ")
print("Run time= {0}s".format(total))
print("Run time= {0}m".format(totalm))
print(" ")
                

# Create DataFrame    
df=pandas.DataFrame(l)
#df 

# Write To Csv File - need to manually change name otherwise old file will be overwritten
df.to_csv("Property24_ToRent_Apartments_CapeTown_Scrap_1.csv")
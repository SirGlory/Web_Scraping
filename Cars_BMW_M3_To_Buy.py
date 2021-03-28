# Imports
import requests
from bs4 import BeautifulSoup
import pandas
import time

# Create Variables
t0 = time.time()
r=requests.get("https://www.cars.co.za/searchVehicle.php?new_or_used=&make_model=BMW%5BM3%5D&vfs_area=&agent_locality=&price_range=&os=&locality=&commercial_type=&body_type_exact=&transmission=&fuel_type=&login_type=&mapped_colour=&vfs_year=&vfs_mileage=&vehicle_axle_config=&keyword=&sort=vfs_price", 
               headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content
soup=BeautifulSoup(c,"html.parser")
all=soup.find_all("div",{"class":"item clearfix vehicle-list__item"})
l=[]
base_url= "https://www.cars.co.za/searchVehicle.php?new_or_used=&make_model=BMW%5BM3%5D&vfs_area=&agent_locality=&price_range=&os=&locality=&commercial_type=&body_type_exact=&transmission=&fuel_type=&login_type=&mapped_colour=&vfs_year=&vfs_mileage=&vehicle_axle_config=&keyword=&sort="

# For Loop running through each page and pulling content
for page in range(1,5,1):
    print(base_url+"&P="+str(page))
    r=requests.get(base_url+"&P="+str(page))
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("div",{"class":"item clearfix vehicle-list__item"})
    
    # For Loop drawing each attribute from specific HTML division
    for item in all :
        d={}
        d["Price"]=item.find("span",{"class":"price vehicle-list__vehicle-price"}).text.replace("\n","").replace(" ","").replace("\t","").replace("\xa0"," ")
        d["Title"]=item.find_all("a",{"class","vehicle-list__vehicle-name"})[0].text.replace("\n","").replace("\t","")
        d["Year"]=item.find_all("li",{"class","vehicle-list__vehicle-attr vehicle-list__ie7icon-0"})[0].text
        d["Mileage"]=item.find_all("li",{"class","vehicle-list__vehicle-attr vehicle-list__ie7icon-1"})[0].text.replace("\xa0"," ")
        d["Transmission"]=item.find_all("li",{"class","vehicle-list__vehicle-attr vehicle-list__ie7icon-2"})[0].text
        d["Fuel Type"]=item.find_all("li",{"class","vehicle-list__vehicle-attr vehicle-list__ie7icon-3"})[0].text
        d["Location"]=item.find_all("div",{"class","vehicle-type-locality vehicle-list__vehicle-location"})[0].text.replace("\n","")            
            
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
df.to_csv("Cars_BMW_M3_Scrap_1.csv")
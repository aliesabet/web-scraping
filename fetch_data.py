import requests
from bs4 import BeautifulSoup
import mysql.connector
import csv
my_db=mysql.connector.connect(user='root',password='Software92')
my_curser=my_db.cursor(buffered=True)
my_curser.execute('CREATE DATABASE IF NOT EXISTS Car_Features')
my_curser.execute('USE Car_Features')
my_curser.execute('CREATE TABLE IF NOT EXISTS CAR(name VARCHAR(255),milage VARCHAR(255),location VARCHAR(255),interior_color VARCHAR(255),exterior_color VARCHAR(255),accident_st VARCHAR(255),price VARCHAR(255))')
my_curser.execute('CREATE TABLE IF NOT EXISTS PAGES(PAGE INT(5))')
my_curser.execute('CREATE TABLE IF NOT EXISTS LASTPAGE(last VARCHAR(255))')
names=[]
milage_value=[]
prices=[]
locations=[]
exterior_colors=[]
interior_colors=[]
acc_status=[]

my_curser.execute('SELECT  * FROM LASTPAGE')
last_page=my_curser.fetchone()
if last_page==None:
    last_page=1
else:
    my_curser.execute('SELECT  * FROM LASTPAGE')
    last_page=my_curser.fetchone()
    last_page=int(last_page[0])+1

    for page in range (last_page,100):
    url=f'https://www.truecar.com/used-cars-for-sale/listings/?dealType=loan&downPayment=3000&monthlyPaymentHigh=500&page={page}'
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    print(res)

    location_of_cars=soup.find_all('div',attrs={"class":"vehicle-card-location mt-1 text-xs","data-test":"vehicleCardLocation"})
    name_of_cars=soup.find_all('div',attrs={'data-test':"vehicleCardYearMakeModel",'class':"vehicle-card-header w-full"})
    price_of_cars=soup.find_all('span',attrs={'data-test':"vehicleListingPriceAmount"})
    mileage_element=soup.find_all('div',attrs={'data-test': 'vehicleMileage'})
    color_of_cars=soup.find_all('div',attrs={'class':"vehicle-card-location mt-1 truncate text-xs",'data-test':"vehicleCardColors"})
    accident_status=soup.find_all('div',attrs={'data-test':"vehicleCardCondition"})

    for p in range(0,len(mileage_element)):
        milage_value.append(mileage_element[p].text)


    for p in range (0,len(name_of_cars)):
        name_of_cars[p]=name_of_cars[p].text.split()[1:3]
        name_of_cars[p]=' '.join(name_of_cars[p])
        names.append(name_of_cars[p])


    for p in range (0,len(price_of_cars)):
        prices.append(price_of_cars[p].text)


    for p in range(0,len(location_of_cars)):
        locations.append(location_of_cars[p].text)


    for p in range (0,len(color_of_cars)):

        exterior_colors.append(color_of_cars[p].text.split(',')[0])
        interior_colors.append(color_of_cars[p].text.split(',')[1])
    
    for p in range (0,len(accident_status)):
        acc_status.append(accident_status[p].text.split(',')[0])


    my_curser.execute(f'SELECT * FROM PAGES WHERE PAGE={page}')
    fech_page=my_curser.fetchone()
    if fech_page is None:
        my_curser.execute(f'INSERT INTO PAGES (PAGE) VALUES ({page})')
        my_db.commit()

        my_curser.execute('SELECT * FROM PAGES ORDER BY PAGE DESC')
    # my_curser.execute('SELECT * FROM PAGES ORDER BY CAST(PAGE AS SIGNED) DESC')

    last_page_result=my_curser.fetchone()
    last_page=last_page_result[0]          
    print(last_page)
    my_curser.execute('SELECT * FROM LASTPAGE')
    fech_last_page=my_curser.fetchone()

    if fech_last_page is None or fech_last_page==1:
        my_curser.execute(f'INSERT INTO LASTPAGE (last) VALUES ({last_page})')
    else:
        my_curser.execute(f'UPDATE LASTPAGE SET last={last_page}')




    for j in range(0,len(names)):
        select_query = f'SELECT * FROM CAR WHERE name="{names[j]}"  AND milage="{milage_value[j]}" AND location="{locations[j]}" AND interior_color="{interior_colors[j]}" AND exterior_color="{exterior_colors[j]}" AND accident_st="{acc_status[j]}" AND price="{prices[j]}"'
        my_curser.execute(select_query)
        feched_row=my_curser.fetchone()
        if feched_row is None:
            my_curser.execute(f'INSERT INTO CAR (name,milage,location,interior_color,exterior_color,accident_st,price) VALUES ("{names[j]}","{milage_value[j]}","{locations[j]}","{interior_colors[j]}","{exterior_colors[j]}","{acc_status[j]}", "{prices[j]}")')
            my_db.commit()



query = "SELECT * FROM CAR"
my_curser.execute(query)

with open('car_res.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    columns = [i[0] for i in my_curser.description]
    writer.writerow(columns)

    for row in my_curser:
        writer.writerow(row)

my_db.commit()
my_db.close()    
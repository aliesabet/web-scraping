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

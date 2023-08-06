print("Made by Sakurai07")
print("https://github.com/sakurai07/")
from googleapi import google
import os
import time
import asyncio
dots = 1
num_page = 1
dp = 1
def ser(q, num_page):
    dots = 1
    search_results = google.search(q, num_page)
    while search_results == []:
        c()
        dots += 1 
        if dots == 0:
            print("(|)loading")
        elif dots == 1:
            print("(/)loading.")
        elif dots == 2:
            print("(-)loading..")
        elif dots == 3:
            print("(\)loading...")
            dots = 0
        search_results = google.search(search, num_page)
    c()
    for result in search_results:
        print()
        print(result.name)
        print()
        print("description:",result.description)
        print()
        print("link:",result.link)
    print()
    print("page",num_page)
def c():
    os.system("clear")
while True:
    num_page = 1
    search = input("search google.py: ")
    print("querying...")
    search_results = google.search(search, num_page)
    while search_results == []:
        
        c()
        
        dots += 1 
        if dots == 0:
            print("(|)loading")
        elif dots == 1:
            print("(/)loading.")
        elif dots == 2:
            print("(-)loading..")
        elif dots == 3:
            print("(\)loading...")
            
            dots = 0
        search_results = google.search(search, num_page)
    c()
    for result in search_results:
        print()
        print(result.name)
        print()
        print("description:",result.description)
        print()
        print("link:",result.link)
    print()
    print("page:",num_page)
    while True:
        print("type n for new tab, np for next page and lp for last page")
        men2 = input(">")
        if men2 == "n":
            num_page = 1
            search = input("search google.py: ")
            print("querying...")
            search_results = google.search(search, num_page)
            while search_results == []:
                c()
                dots += 1 
                if dots == 0:
                    print("(|)loading")
                elif dots == 1:
                    print("(/)loading.")
                elif dots == 2:
                    print("(-)loading..")
                elif dots == 3:
                    print("(\)loading...")
                    dots = 0
                search_results = google.search(search, num_page)
            c()
            for result in search_results:
                print(result.name)
                print()
                print("description:",result.description)
                print()
                print("link:",result.link)
            print()
            print("page number:",num_page)
        elif men2 == "np":
            dp += 1
            ser(search, dp)
        elif men2 == "lp":
            if dp != 0:
                dp -= 1
                ser(search,dp)
            else:
                dp = dp
                ser(search, dp)
            
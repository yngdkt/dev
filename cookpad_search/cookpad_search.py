# -*- coding: utf-8 -*-

import urllib2
import math
from bs4 import BeautifulSoup

RECIPE_PER_LIST = 10

def get_tsukurepo_count_from_recipe(url_text):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    #html = opener.open("https://cookpad.com/recipe/1069312")
    html = opener.open(url_text)
    soup = BeautifulSoup(html, "html.parser")
    tsukurepo_count = soup.find("span", attrs={"class": "tsukurepo_count"})

    if isinstance(tsukurepo_count,type(None)):
        return 0
    else:
        tsukurepo_count_int = int(tsukurepo_count.string.replace(",",""))
        return tsukurepo_count_int


def get_recipe_list_from_search_page(search_page_url):
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    search_html = opener.open(search_page_url)
    soup = BeautifulSoup(search_html, "html.parser")
    
    all_link_list = soup.find_all('a', attrs={"class":"recipe-title"})

    recipe_link_list = []
    
    for link in all_link_list:
        href_string = link.get("href")
        if (not isinstance(href_string,type(None))) and "/recipe/" in href_string:
            recipe_link_list.append(href_string)

    return recipe_link_list

def get_search_pages_urls(search_page_url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
    search_html = opener.open(search_page_url)
    
    soup = BeautifulSoup(search_html, "html.parser")
    search_count_div = soup.find("div", "count")
    #print(search_count_div.em.string)
    search_count = int(search_count_div.em.string[:-1])
    print "found " + str(search_count) + "recipes..."
    result_url_list = []
    num_page = int(math.ceil(search_count / RECIPE_PER_LIST))+1
    search_page_url_base = search_page_url.split("?")[0]
    
    for ii in range(num_page):
        if ii == 0:
            result_url_list.append(search_page_url_base)
        else:
            result_url_list.append(search_page_url_base + "?page=" + str(ii))
    return result_url_list
    
test = "https://cookpad.com/search/%E3%81%9F%E3%81%93%20%E3%82%A2%E3%83%92%E3%83%BC%E3%82%B8%E3%83%A7%20%E3%82%AD%E3%83%8E%E3%82%B3"
search_page_url_list = get_search_pages_urls(test)
recipe_link_list = []

for search_page_url in search_page_url_list:
    recipe_list_for_page = get_recipe_list_from_search_page(search_page_url)
    print recipe_list_for_page
    recipe_link_list = recipe_link_list + recipe_list_for_page

print len(recipe_link_list)

result = {}
for recipe_link in recipe_link_list:
    result[recipe_link] = get_tsukurepo_count_from_recipe("https://cookpad.com" + recipe_link)
print result

f = open("result.txt", "w")
f.write(result)
f.close()

#recipe_link_list = get_recipe_list_from_search_page(test)


#recipe_tsukurepo_count = []
#for link in recipe_link_list:
#    recipe_tsukurepo_count.append(get_tsukurepo_count_from_recipe( "https://cookpad.com" + link))
#print recipe_tsukurepo_count
    
#hoge = get_tsukurepo_count("https://cookpad.com/recipe/1069312")
#print hoge

#f = open("search_result.txt","r")
#search_html = f.read()
#f.close()
#soup = BeautifulSoup(search_html, "html.parser")
#search_count_div = soup.find("div", "count")
#print(int(search_count_div.em.string[:-1]))
 


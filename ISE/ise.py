import requests
from bs4 import BeautifulSoup
import re
import json
import datetime
from rfeed import *
import ast

detailed_list = []
path = "/home/Augists/RSSforSSDUT/ISE/"
# update_list = []

class ise():
    def __init__(self):
        '''
        initialize:
            link
            headers
        '''
        self.link = "https://drise.dlut.edu.cn/ywgg/xytz.htm"
        self.header = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"}

    def start(self):
        '''
        requests:
            get undergradution notification document
        '''
        undergraduation_response = requests.get(url=self.link, headers=self.header)
        if undergraduation_response.status_code == 200:
            self.response200(undergraduation_response)
        else:
            print("Wrong Status Code")

    def response200(self, response):
        '''
        response handle:
            utf-8 encoding
            get detailed link
        '''
        res_content = response.content
        res_doc = str(res_content,'utf-8')
        soup = BeautifulSoup(res_doc, 'html.parser')
        under_list = soup.find(class_='list')
        if self.update_or_not(under_list):
            print("Updating")
            # under_li = under_list.findAll('li')
            # for li in under_list.find_all('li'):
            under_li = under_list.find_all('li')
            for index, li in enumerate(under_li[0:7]):
                a_href = li.find('a', href=True)
                found_url = re.split(r'(https?:\/\/.*?)', a_href['href'])
                detailed_url = "https://drise.dlut.edu.cn/" + found_url[0]
                if self.not_new_link(detailed_url):
                    break
                self.get_details(index+1, detailed_url)
        else:
            print("No Update This Time")

    def update_or_not(self, under_list):
        '''
        check:
            check first li item should update or not
                using title text
                using link
            update global value detailed_list for not_new_link function
        '''

        '''link'''
        global path
        local_path = path + "info.txt"
        f = open(local_path, "r")
        lines = f.readlines()

        # read first link for check
        first_link = lines[0][:-1]
        print("Link in file: " + first_link)

        # # update gloabal value detailed_list for not_new_link
        # global detailed_list
        # # detailed_list = lines[1:]
        # for detail in lines[1:]:
        #     detailed_list.append(detail)

        f.close()

        cur_first = under_list.find('li')
        cur_un_link = cur_first.find('a', href=True)
        cur_link = re.split(r'(https?:\/\/.*?)', cur_un_link['href'])[0]
        print("Link on website: " + cur_link)
        if cur_link == first_link:
            return False    # No need update
        else:
            self.set_first_link(cur_link)
            return True

        '''title text error'''
        # f = open("info.txt", "r")
        # first_title = f.readlines()
        # print(first_title)
        # total_title = ""
        # for f_line in first_title:
        #     total_title += f_line
        # f.close()
        # print(total_title)
        # cur_first = under_list.find('li').get_text()
        # print(cur_first)
        # if cur_first == first_title:
        #     return False
        # else:
        #     self.set_first_title(cur_first)
        #     return True

    def set_first_link(self, link):
        '''
        update:
            save the current first item link in the info file
        '''
        global path
        local_path = path + "info.txt"
        f = open(local_path, "w")
        f.write(link+"\n")
        global detailed_list
        for i in detailed_list:
            f.write(i)
        # f = open("info.txt", "r")
        # list_of_lines = f.readlines()
        # list_of_lines[0] = link + "\n"
        # print("set first link")

        # f = open("info.txt", "w")
        # f.writelines(list_of_lines)
        f.close()

    # def set_first_title(self, title):
    #     '''
    #     update:
    #         save the current first li item in the info file
    #         error in using title
    #     '''
    #     f = open("info.txt", "w")
    #     f.write(title)
    #     f.close()

    def not_new_link(self, link):
        '''
        check:
            check detailed link exist or not
        '''
        global detailed_list
        # print(detailed_list)
        for i in detailed_list:
            temp_dic = json.loads(i)
            if temp_dic['url'] == link:
                return True
        return False

    def get_details(self, i, url):
        '''
        requests:
            get detailed information
            storge in detailed_item as dictionary
        '''
        detailed_item = {}
        detailed_res= requests.get(url=url, headers=self.header)
        detailed_content = detailed_res.content
        detailed_doc = str(detailed_content,'utf-8')
        detailed_soup = BeautifulSoup(detailed_doc, 'html.parser')
        detailed_title = detailed_soup.find(class_='header').get_text()
        # detailed_item['number'] = i     # DEBUG
        detailed_item['title'] = detailed_title
        detailed_item['url'] = url

        # save value to update_list for rss_push
        # global update_list
        # update_list.append(detailed_item)

        # write into info.txt for log
        self.write_json(detailed_item)
        # print(rss_list)

    def write_json(self, detailed_item):
        '''
        write file:
            write to the rss file in json
        '''
        print("Writing as json to info.txt")
        global path
        local_path = path + "info.txt"
        with open(local_path, 'a') as f:
            # json.dump(rss_list, f, indent=4, ensure_ascii=False)
            json.dump(detailed_item, f, ensure_ascii=False)
            f.write("\n")

    def rss_push(self):
        '''
        RSS:
            push rss
        '''
        print("RSS Generating\n")
        itemsList = []
        global path
        local_path = path + "info.txt"
        with open(local_path, 'r') as f:
            for iread in f.readlines()[1:]:
                i = ast.literal_eval(iread)
                item = Item(
                        title = i['title'],
                        link = i['url'],
                        # description = str(i['number']) + ": " +
                        description = i['title'] + "\n" + i['url'],
                        author = 'Augists',
                        guid = Guid(i['url']),
                        # DEBUG: need update time
                        pubDate=datetime.datetime(2021, 8, 1, 4, 0))
                itemsList.append(item)
        feed = Feed(
                title = "ISE Undergraduate Notification",
                link = "http://137.116.167.187/ise/atom.xml",
                description = "RSS atom.xml of https://drise.dlut.edu.cn/",
                language = "en-US",
                lastBuildDate = datetime.datetime.now(),
                items = itemsList
                )
        atom = feed.rss()
        with open('/var/www/html/ise/atom.xml', 'w') as f:
            f.write(atom)

'''
sequence:
    __init__
    start
        response
            update_or_not
                set_first_link
                not_new_link
            get_details
                write_json
    rss_push
'''
s = ise()
s.start()
s.rss_push()


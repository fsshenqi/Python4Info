# -*- coding: utf-8 -*-
import urllib2
import urllib
import copy
import re
import json
import sqlite3

from pyquery import PyQuery as pq
import sys
reload(sys)
sys.setdefaultencoding('utf8')
class YunJCJG():
    id = ""
    name = ""
    data_dict = {}
    def __init__(self, name):
        self.name = name
        self.data_dict = copy.copy(YunJCJG.default_data_dict)
        self.data_dict["_ctl0:ContentPlaceHolder1:txt机构名称"] = self.name
        ids = query_id_by_name(self.name)
        self.id = ids[0][0] if len(ids) == 1 else None

    def get_id_by_name(self):
        req = urllib2.Request(YunJCJG.host_url)
        data = urllib.urlencode(self.data_dict)
        req.add_header("Content-Type","application/x-www-form-urlencoded")
        req.add_data(data)
        results = urllib2.urlopen(req).read()
        list = parse_name_id_list(results)
        for t in list:
            if t[0] == self.name:
                self.id = t[1]
            print t[0],":",t[1]

    def get_info_dict(self):
        url = YunJCJG.info_url + "?" + urllib.urlencode({"id":self.id})
        page = pq(urllib2.urlopen(url).read())
        info_dict = {}
        for title in page("strong"):
            name = pq(title).text().strip().decode().replace("：","").strip()
            name = YunJCJG.info_title_map[name]
            value = pq(title).parent().next("td").text().strip().decode()
            info_dict[name] = value
        return info_dict

def save_results(results):
    file = open("result.html","wb")
    file.write(results)
    file.close();

"""从网页中提取检测机构名称及配对ID

"""
def parse_name_id_list(results):
    name_id_list = []
    try:
        main_page = pq(results)
        trs = main_page("div.search_form2_full tr")
        for tr in trs[1:-1]:
            try:
                name = pq(pq(tr).children("td")[1]).text()
                id = pq(tr).children("td a").attr("href")
                id = re.findall("id=([^=\s]+)", id)[0]
                name_id_list.append((name,id))
            except:
                pass
    except:
        pass
    return name_id_list

def rebulid_name_id_db(list):
    conn = sqlite3.connect("jcjg.sqlite3")
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS T_JCJG ')
    cur.execute('CREATE TABLE T_JCJG (name TEXT, yun_id TEXT)')
    for t in list:
        cur.execute('INSERT INTO T_JCJG (name, yun_id) VALUES (?,?)', t)
    conn.commit()
    conn.close()



def query_db_id_by_name(name):
    conn = sqlite3.connect(YunJCJG.database)
    cur = conn.cursor()
    cur.execute('SELECT yun_id, name FROM T_JCJG WHERE name like (?)', ("%"+unicode(name)+"%",))
    results = [(t[0], t[1]) for t in cur]
    conn.close()
    return results

def query_web_id_by_name(name):
    req = urllib2.Request(YunJCJG.host_url)
    m_data_dict = copy.copy(YunJCJG.data_dict)
    m_data_dict["_ctl0:ContentPlaceHolder1:txt机构名称"]=name
    data = urllib.urlencode(m_data_dict)
    req.add_header("Content-Type","application/x-www-form-urlencoded")
    req.add_data(data)
    results = urllib2.urlopen(req).read()
    list = parse_name_id_list(results)
    return list

def query_id_by_name(name):
    return query_db_id_by_name(name) or query_web_id_by_name(name)

YunJCJG.database = "jcjg.sqlite3"
YunJCJG.host_url = "http://www.jtsyjc.net/SearchOrgan.aspx"#交通部资质
#TODO 住建部检测资质
YunJCJG.info_url = "http://www.jtsyjc.net/OrganSite/ShowOrganInfo.aspx"
YunJCJG.person_url = "http://www.jtsyjc.net/OrganSite/ShowOrganPersonnel.aspx"
YunJCJG.default_data_dict = {"_ctl0:ContentPlaceHolder1:txt机构名称": "",
                         "_ctl0:ContentPlaceHolder1:DropDownList版本1": "beea29e2-4fc6-4b62-b887-587eca85c8fe",
                         "_ctl0:ContentPlaceHolder1:drop省": "",
                         "_ctl0:ContentPlaceHolder1:DropDownList专业1": "",
                         "_ctl0:ContentPlaceHolder1:drop资质等级": "",
                         "_ctl0:ContentPlaceHolder1:imgbt1.x": "10",
                         "_ctl0:ContentPlaceHolder1:imgbt1.y": "18",
                         "__VIEWSTATE": "if43aMGz3uoCcRQ+TXHNHoChDOIN4OQnn3w7ZaFE0paP9+KKqcemLnpF4ZKgPt3Cw4SublOx20BoViFDhJ/V4bDU4s+lWBna5sQHkiDVn8ub2Lz1JYtvoezIedkTut+bFMgMqzzcFe67zSemI53uKLFZGu/K2cIvbXgdBZKOpgM1k8II+wyXp6Q8rLvYNC8ljw8yCgXGlYEf/YdrRtisbH7zd9FKrDhIqkVk9y/fKCdcyrpps9YaGjcsjnznBT+ZuLglP/8DQ52AtwSXw3CcqwQC18pforCTcK63Wi7q33IIhumljswz6IIBohseI4yGwt7yK3vZKINt1CtOwYlUKf9S3n6ElFyuu1GnBRnvA5qtVWfmAwVfnAMWppUgY7AOv7ycQ0h23bPbLMGT2pMlPa9YhCSwsy1DoOWsSa5bRCfHoWJKPK6kwlyQNAMegz7C0CIT4kDmTbXXQrqYAFExyMvasXj8jQ63TLuh+UvfhuXiZNAe0Jd5C0U97qrfjTyM6DI7bdHP3vHm387HeTSqIT8QBCE6VWhyQGScEfBsMX1w29EpBGWIFL1lIVzhus/fElF0x4JxLwNqDr/q99jdIkos0+mwO3OP2m0yTlp0KSgdjjYcNWcc7rwlooqcBhDhobsrIgd1AeIL1Dr1oG3z/ei+6F6DVbEyrWbWj5dFveu697rVw7jXkAnc5HgAcic4nwi1q8iRcBiEMoqCYugQV9SyWjT0/wTZrMDmAoWv8WdC4h+m8SyXbhM0msOc20vwnrOejcUhLi1HnacNcvX2p2Kdmle7l96GRnz1hQ+Eep7oh5kqu4M4weu5ANSiJT3E8rQ0ncgEsqmV4Lf5303zwrRn9cVvo1lfnU9ouZAnK1w1hhiygND1bJTgjVNBqYUgYjRVQFseaMbD/YFaeHMgePibRCHkg+gKYMaZE2EH+jDKuYPYlwscYIHh31ZHQEq+sT9L98rO6A/7B2hPJdBQ8+1S990rIatKny3AkdJwqZsk7EiDQy7FUJ/1t9EQTPNN",
                         "__EVENTVALIDATION":"UcO+LF51Wv5bgQkhZ3KAjaz2F6/kq/ghaLqDy6cHEjnbHwdswCbEM+yxeB7Q0+ZtpMT1fip7US//L5MsA0SGJl1PtUihlftGD+/pfsOCt1Q00Pqe0VyZksDtBRw8XbMUGsTkBxDrAe+9CFR4gwVqwPYLY5EjKDjHMmAKms9Ry9zO9RiYyZphDQqcZNSpIlXPAHSJZfV3uiU5PG+HneBAItldp3absrGTmAe8wD8xPSmeVP142GAJ0SuxZOZnpynGfg6yRyKSGAPPFa2rwJyLkjCuDs155UYgG2wNQmbfhTQ=",
             }
YunJCJG.info_title_map = {u"机构名称":"name",
                        u"机构性质":"type",
                        u"所在省(市)":"province",
                        u"所在市（区）":"city",
                        u"法定代表人":"representative",
                        u"行政负责人":"administrator",
                        u"通讯地址":"address",
                        u"邮编":"code",
                        u"联系电话":"telephone",
                        u"传真":"fax",
                        u"邮箱":"email",
                        u"网址":"website",
                        u"成立时间":"founding_time",
                        u"注册资本（万）":"registered_capital",
                        u"营业执照 有效期至":"valid_until_date",
                        u"营业执照注册号":"business_licence",
                        u"简介":"introduction",}

print query_id_by_name("佛山市公路桥梁工程监测站")
fsjcz = YunJCJG("佛山市公路桥梁工程监测站")


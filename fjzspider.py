#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-18 13:28:37
# @Author  : LvGang/Garfield.lv
# @Link    : lvgang@shtdtech.com
# @Version : $Id$

import os
import re
import json
import requests
from lxml import etree


class FJZbk(object):
    """docstring for FJZbk"""
    def __init__(self):
        super(FJZbk, self).__init__()
        self.main_url = 'http://www.fanjian.net/jbk'
        self.headers = {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cache-Control":"max-age=0",
            "Connection":"keep-alive",
            "Cookie":"sessfj=2899548fba949195507f506beb461bcf46c2b4f3; BAIDU_SSP_lcr=https://www.baidu.com/link?url=X_IiYHR_8JQPUBkkf7cTej-cJMwSkFyC9FhswJ15jbEUoRJBvqv1W2SFi7P84mSS&wd=&eqid=cbded3610009754e000000035c6a3fb4; Hm_lvt_9e63a3a5b934d31b225a20be89b10904=1550467005; mp_bdlvt_t=3c8620359585d5; Hm_lpvt_9e63a3a5b934d31b225a20be89b10904=1550468881; amvid=c5f31a7f9595ae61e3e11ec7e0605856",
            "Host":"www.fanjian.net",
            "Referer":"http://www.fanjian.net/",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",

        }
        self.fp = open('./hotwords.json','w',encoding='utf-8')
        self.fp.write('{\n')

    def response_handle(self,url):
        '''
        说明：根据传入的url构造响应
        输入：url,String,网址
        输出：Response，Response Object，响应结果的对象

        '''
        response = requests.get(url=url,headers=self.headers)
        return response

    def parse_words(self,response):
        '''
        说明：传入响应结果，解析得到网络热词及其解析页面的url
        输入：response，Response Object，网址响应结果的对象
        输出：wordlist,list,网络热词及URl构造的list，数据格式[{'word':'word','url':'url'},{},{}]
        '''
        html = etree.HTML(response.text)
        words = html.xpath("//ul[@class='word-list']/li/dl[@class='clearfix']/dd/a")
        res = [{'word':w.xpath("./text()")[0],'url':w.xpath("./@href")[0]} for w in words]
        return res

    def parse_info(self,response):
        # print(response.text)
        # content = re.findall(r'<div class="view-main">(.*)</div>',response.text)
        # print(content)
        html = etree.HTML(response.text)
        info_tmp = ''.join(html.xpath("//div[@class='view-main']//text()"))
        imgs = html.xpath("//div[@class='view-main']/p/img/@src")
        # bkgd = html.xpath("//div[@class='bkgd-topapps']//text()")
        print(info_tmp)
        print(imgs)
        return info_tmp,imgs



    def main(self):
        word_response = self.response_handle(self.main_url)
        res = self.parse_words(word_response)
        for wd in res:
            word = wd['word']
            url = wd['url']
            print('======================')
            print(word)
            infores = self.response_handle(url)
            info,imgs = self.parse_info(infores)
            self.fp.write(json.dumps({'word':word,'info':info,'imgs':imgs},ensure_ascii=False)+',\n')
        self.fp.write('}')
        self.fp.close()

if __name__ == '__main__':
    f = FJZbk()
    f.main()

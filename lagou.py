#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: tracyqan time:2019/3/29

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import pandas as pd
import time

class LagouSpider():

    def __init__(self):
        self.driver_path = r'E:\chromedriver.exe'
        self.driver = webdriver.Chrome(executable_path=self.driver_path)
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.data = []

    def get_detail_content(self):

        salary = self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[1]').text.replace('/', '').strip()
        address = self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[2]').text.replace('/', '').strip()
        work_years = self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[3]').text.replace('/', '').strip()
        education = self.driver.find_element_by_xpath('//dd[@class="job_request"]//span[4]').text.replace('/', '').strip()
        advantage = self.driver.find_element_by_xpath('//dd[@class="job-advantage"]/p').text
        requirment = self.driver.find_element_by_xpath('//div[@class="job-detail"]').text

        job_dict = {
            'salary': salary,
            'address': address,
            'work_years': work_years,
            'education': education,
            'advantage': advantage,
            'requirement': requirment,
        }

        self.data.append(job_dict)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


    def run(self):
        self.driver.get(self.url)
        try:
            while True:
                detail_urls = self.driver.find_elements_by_xpath('//a[@class="position_link"]')
                for each in detail_urls:
                    try:
                        each.click()
                    except WebDriverException:
                        self.driver.execute_script("arguments[0].scrollIntoView();", each)  # 页面移动到元素与顶部对齐
                        each.click()
                    self.driver.switch_to.window(self.driver.window_handles[1]) # 切换窗口句柄到新打开的页面
                    # print(self.driver.current_url)
                    self.get_detail_content()
                    time.sleep(0.5)
                try:
                    next_page = self.driver.find_element_by_xpath('//span[@action="next"]')
                    next_page.click()
                except:
                    break
                else:
                    time.sleep(1)
        except:
            print('访问过于频繁,页面跳转', self.driver.current_url)
        finally:
            df = pd.DataFrame(self.data)
            df.to_csv('job.csv')
            self.driver.quit()


if __name__ == '__main__':
    lagou = LagouSpider()
    lagou.run()
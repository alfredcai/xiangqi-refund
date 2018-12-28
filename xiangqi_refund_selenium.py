# -*- coding: utf-8 -*-
import datetime
import logging
import sys
import time

from selenium import webdriver

HOST = "http://gis1z4xshb2s37ki.mikecrm.com"


def do_request(username, mobile):
    logging.info(
        "request form with username:%s, mobile:%s" % (username, mobile))
    do_chrome_submit(username, mobile)


def do_chrome_submit(username, mobile):
    options = get_chrome_options()

    client = webdriver.Chrome(
        chrome_options=options, executable_path=CHROME_DRIVER_PATH)

    path = "/JI5p0O4"
    url = HOST + path

    mobile_input, name_input, submit_button = get_web_form(client, url)

    name_input.send_keys(username)
    mobile_input.send_keys(mobile)
    submit_button.click()
    logging.info("submit button click with username:%s, mobile:%s" % (username, mobile))

    check_chrome_submit_result(client)
    client.quit()


def get_web_form(client, url):
    client.get(url)
    try:
        inputs = client.find_elements_by_tag_name("input")
        name_input = inputs[0]
        mobile_input = inputs[1]
        submit_button = client.find_element_by_id("form_submit")
    except Exception as e:
        logging.error(e)
        logging.error("can't find web page's elements, pls check the page url")
        client.quit()
        sys.exit()
    return mobile_input, name_input, submit_button


def get_chrome_options():
    USER_AGENT = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.0.54_r849063.501 NetType/WIFI"

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--user-agent=" + USER_AGENT)
    return options


def check_chrome_submit_result(client):
    logging.info("check ing submit result %s" % str(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    time.sleep(5)
    try:
        result = client.find_element_by_xpath(
            u"//html/body/form/div/div[1]/div[2]/div/div[2]/div[1]").text
    except Exception as e:
        logging.error(e)

    if result:
        logging.info("submit result:" + result)
    else:
        logging.warning("submit result:" + result)
        logging.WARNING("submit failed")


def get_file_path():
    system = sys.platform
    logging.info("system platform is " + system)
    return {
        "darwin": ("/Users/alfredcai/CodeProjects/ReleasesProgram/selenium/chromedriver", "./logger.log"),
        "linux": ("/root/xiangqi/chromedriver", "/root/xiangqi/log/xiangqi.log")
    }.get(system, ("/Users/alfredcai/CodeProjects/ReleasesProgram/selenium/chromedriver", "./logger.log"))


def set_logging_config(log_file_path):
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"

    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format=fmt,
        datefmt=datefmt)


if __name__ == '__main__':
    CHROME_DRIVER_PATH, LOGGER_FILE_PATH = get_file_path()
    set_logging_config(LOGGER_FILE_PATH)

    logging.info("args lens: %d" % len(sys.argv))
    arg_username = str(sys.argv[1])
    arg_mobile = str(sys.argv[2])

    logging.info("args username: %s, mobile: %s" % (arg_username, arg_mobile))
    logging.info("do request at %s" % str(
        datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    do_request(arg_username, arg_mobile)

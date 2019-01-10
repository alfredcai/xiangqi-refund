# -*- coding: utf-8 -*-
import logging
import sys
import time
from datetime import datetime

from selenium import webdriver

# url = "http://gis1z4xshb2s37ki.mikecrm.com/JI5p0O4"
url = "http://gis1z4xshb2s37ki.mikecrm.com/dRWXuZW"
submit_count_max = 100


def do_request(username, mobile, time="09:00:00"):
    options = get_chrome_options()

    client = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)

    try:
        do_test(client)
    except Exception as e:
        logging.error(e)

    submit_count = 0
    while True:
        if check_request_time(time):
            logging.info("starting submit form with username:%s, mobile:%s" % (username, mobile))
            do_chrome_submit(client, username, mobile)
            submit_count = submit_count + 1
            if submit_count >= submit_count_max:
                return 0

    client.quit()


def check_request_time(time="9:00:00"):
    now = datetime.now()
    settled_time = datetime.strptime(time, "%H:%M:%S")
    settled_time = now.replace(hour=settled_time.time().hour,
                               minute=settled_time.time().minute,
                               second=settled_time.time().second,
                               microsecond=0)
    return now > settled_time


def do_chrome_submit(client, username, mobile):
    mobile_input, name_input, submit_button = get_web_form(client)

    name_input.send_keys(username)
    mobile_input.send_keys(mobile)
    submit_button.click()
    logging.info(
        "########################  submit button click with username:%s, mobile:%s"
        % (username, mobile))

    check_chrome_submit_result(client)


def get_web_form(client):
    client.get(url)
    try:
        inputs = client.find_elements_by_tag_name("input")
        name_input = inputs[0]
        mobile_input = inputs[1]
        submit_button = client.find_element_by_id("form_submit")

        logging.debug("get name,mobile input and submit button")
    except Exception as e:
        logging.error(e)
        logging.error("can't find web page's elements, pls check the page url")
        try_find_page_error_info(client)
        client.quit()
        sys.exit()
    return mobile_input, name_input, submit_button


def try_find_page_error_info(client):
    try:
        body = client.find_elements_by_tag_name("body")
        for b in body:
            logging.debug(b.text)

        form_list = client.find_elements_by_tag_name("form")
        for f in form_list:
            logging.error(f.text)
    except Exception:
        pass


def get_chrome_options():
    user_agent = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.0.54_r849063.501 NetType/WIFI "

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--user-agent=" + user_agent)
    return options


def check_chrome_submit_result(client):
    logging.info("checking submit result")
    time.sleep(5)
    try:
        result = client.find_element_by_xpath(
            u"//html/body/form/div/div[1]/div[2]/div/div[2]/div[1]").text
    except Exception as e:
        logging.error(e)

    if result:
        logging.info("******************* submit result:" + result)
    else:
        logging.warning("******************* submit result:" + result)
        logging.WARNING("******************* submit failed")


def get_file_path():
    system = sys.platform
    logging.debug("system platform is " + system)
    config_dir = {
        "darwin":
            ("/Users/alfredcai/CodeProjects/ReleasesProgram/selenium/chromedriver",
             "./logger.log"),
        "linux": ("/root/xiangqi/chromedriver",
                  "/root/xiangqi/log/xiangqi.log")
    }
    return config_dir.get(system, config_dir.get("darwin"))


def set_logging_config(log_file_path):
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"

    logging.root.handlers = []
    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format=fmt,
        datefmt=datefmt)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))
    logging.getLogger("").addHandler(console)


def do_test(client):
    client.get(url)
    assert client.title == '诚信金退款申请登记', "test request page title is incorrect"
    logging.info("test request page is success")


if __name__ == '__main__':
    CHROME_DRIVER_PATH, LOGGER_FILE_PATH = get_file_path()
    set_logging_config(LOGGER_FILE_PATH)

    logging.debug("chrome driver path:%s" % CHROME_DRIVER_PATH)
    logging.debug("logging file locale at:%s" % LOGGER_FILE_PATH)

    try:
        arg_username = str(sys.argv[1])
        arg_mobile = str(sys.argv[2])
        arg_request_time = str(sys.argv[3])
    except IndexError as e:
        logging.error("input args are incorrect")
        sys.exit(0)

    logging.info("args lens:%d, detail:%s" % (len(sys.argv), sys.argv))

    do_request(arg_username, arg_mobile, arg_request_time)

# -*- coding: utf-8 -*-
import logging
import sys
import time
from datetime import datetime

from selenium import webdriver

# url = "http://gis1z4xshb2s37ki.mikecrm.com/JI5p0O4"
# url = "http://gis1z4xshb2s37ki.mikecrm.com/dRWXuZW"
# url = "http://gis1z4xshb2s37ki.mikecrm.com/OceMOu5"
# url = "http://gis1z4xshb2s37ki.mikecrm.com/4qhdO2B"
url = "http://gis1z4xshb2s37ki.mikecrm.com/01irI6d"
form_password = "xq123456"
submit_count_max = 10


def do_request(username, mobile, time="09:00:00"):
    client = restart_client()

    try:
        do_test(client)
    except Exception as e:
        logging.error(e)

    submit_count, error_count = 0, 0
    while True:
        if check_request_time(time):
            logging.info(
                "Starting submit form in %d times with username:%s, mobile:%s" % (submit_count + 1, username, mobile))
            try:
                do_chrome_submit(client, username, mobile)
                submit_count = submit_count + 1
                if submit_count >= submit_count_max:
                    return 0
            except Exception as e:
                error_count += 1
                logging.error("Failed submit form in %d times" % error_count)
                if error_count >= 5:
                    return 0
            client = restart_client(client)
    client.close()


def restart_client(client=None):
    if client:
        client.close()
    options = get_chrome_options()
    client = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)
    return client


def check_request_time(time="9:00:00"):
    now = datetime.now()
    settled_time = datetime.strptime(time, "%H:%M:%S")
    settled_time = now.replace(hour=settled_time.time().hour,
                               minute=settled_time.time().minute,
                               second=settled_time.time().second,
                               microsecond=0)
    return now > settled_time


def do_chrome_submit(client, username, mobile):
    client.get(url)
    submit_enter_password(client)
    time.sleep(1)
    submit_form(client, username, mobile)
    check_chrome_submit_result(client)


def submit_enter_password(client):
    try:
        inputs = client.find_elements_by_tag_name("input")
        name_input = inputs[0]
        submit_button = client.find_element_by_class_name("fbc_button")
        name_input.send_keys(form_password)
        submit_button.click()
        logging.debug("Succeed enter into the form")
    except Exception as e:
        logging.error("Entering form error,password:%s" % form_password)
        raise e


def submit_form(client, username, mobile):
    try:
        inputs = client.find_elements_by_tag_name("input")
        name_input = inputs[0]
        mobile_input = inputs[1]
        submit_button = client.find_element_by_id("form_submit")

        logging.debug("Get name,mobile input and submit button")

        name_input.send_keys(username)
        mobile_input.send_keys(mobile)
        submit_button.click()
        logging.debug("Submit button click with username:%s, mobile:%s" % (username, mobile))
    except Exception as e:
        logging.error("Can't find web page's elements, pls check the page url")
        try_find_page_error_info(client)
        raise e


def try_find_page_error_info(client):
    try:
        body = client.find_elements_by_tag_name("body")
        for b in body:
            logging.debug(b.text.repalce("\n", " "))

        form_list = client.find_elements_by_tag_name("form")
        for f in form_list:
            logging.error(f.text.repalce("\n", " "))
    except Exception:
        logging.error("Unexpected error")


def get_chrome_options():
    user_agent = "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) " \
                 "Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36 MicroMessenger/6.0.0.54_r849063.501 NetType/WIFI "

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--user-agent=" + user_agent)

    prefs = {'profile.default_content_setting_values': {'images': 2}}
    options.add_experimental_option('prefs', prefs)
    return options


def check_chrome_submit_result(client):
    logging.info("Checking submit result")
    time.sleep(5)
    try:
        result = client.find_element_by_xpath(u"//html/body/form/div/div[1]/div[2]/div/div[2]/div[1]").text
    except Exception as e:
        logging.error(e)
        result = ""

    try:
        body = client.find_elements_by_tag_name("body")
    except Exception as e:
        logging.error(e)
        body = []

    if not result:
        for i in body:
            str = i.text.replace("\r", " ")
            result += str.replace("\n", " ")

    if result:
        logging.info("Submit result:%s" % result)
    else:
        logging.error("Failed submit, page result: %s" % result)


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

    info_level_file = logging.FileHandler(filename=log_file_path.replace(".log", "_info.log"))
    info_level_file.setLevel(logging.INFO)
    info_level_file.setFormatter(logging.Formatter(fmt=fmt, datefmt=datefmt))

    logging.getLogger("").addHandler(console)
    logging.getLogger("").addHandler(info_level_file)


def do_test(client):
    client.get(url)
    assert client.title == '诚信金退款申请登记', "test request page title is incorrect"
    logging.info("Test request page is success")


if __name__ == '__main__':
    CHROME_DRIVER_PATH, LOGGER_FILE_PATH = get_file_path()
    set_logging_config(LOGGER_FILE_PATH)

    logging.debug("Chrome driver path:%s" % CHROME_DRIVER_PATH)
    logging.debug("Logging file locale at:%s" % LOGGER_FILE_PATH)

    try:
        arg_username = str(sys.argv[1])
        arg_mobile = str(sys.argv[2])
        arg_request_time = str(sys.argv[3])
    except IndexError as e:
        logging.error("input args are incorrect")
        sys.exit(0)

    logging.info("args lens:%d, detail:%s" % (len(sys.argv), sys.argv))

    do_request(arg_username, arg_mobile, arg_request_time)

#!/usr/bin/env python

import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client


# Returns chromedriver with necessary parameters
def loadDriver():
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        executable_path="/usr/local/bin/chromedriver", options=options
    )

    driver.set_page_load_timeout(15)

    return driver


def sendTwilio(msgBody):
    account_sid = "YOUR KEY HERE"
    auth_token = "YOUR KEY HERE"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=msgBody, from_="YOUR KEY HERE", to="YOUR KEY HERE"
    )


def main():
    search = [13, 18]
    search2 = search
    i = 1

    driver = loadDriver()
    sendTwilio("Beginning script %s" % time.time())

    while True:
        time.sleep(1)
        driver.get(
            "https://www.epicpass.com/api/LiftAccessApi/GetCapacityControlReservationInventory?resortCode=14&startDate=11%2F1%2F2020&endDate=12%2F31%2F2020"
        )
        res = json.loads(driver.find_element_by_tag_name("pre").text)

        for s in search2:
            dt = "2020-12-%sT00:00:00" % s

            if dt not in res["NoInventoryDays"]:
                sendTwilio("Park City %s" % dt)
                search2.remove(s)

        if i % 24 == 0:
            search2 = search

        i += 1

        print("Checked %s: length %s" % (time.time(), len(res["NoInventoryDays"])))


if __name__ == "__main__":
    main()

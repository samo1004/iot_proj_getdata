import requests
import time
import sys
import base64
import datetime

ENDPOINT = "industrial.api.ubidots.com"
DEVICE_LABEL = "weather-station"
VARIABLE_LABEL = "light"
TOKEN = "BBFF-cSE6hmXL81HFKyx6Gw3inoTnhqT6Dp"  # replace with your TOKEN
DELAY = 1  # Delay in seconds

def TimeTrans(timestamp):
    DB_Date = datetime.datetime.fromtimestamp(int(timestamp) / 1000)  # using the local timezone
    DB_Date = DB_Date.strftime("%Y-%m-%d %H:%M:%S")  # 2018-04-07 20:48:08, YMMV
    return DB_Date

def get_Light(url=ENDPOINT, device=DEVICE_LABEL, variable=VARIABLE_LABEL,
              token=TOKEN):
    variable = "light"
    url = "http://{}/api/v1.6/devices/{}/{}/values/?page_size=2".format(url,
                                                                        device,
                                                                        variable)

    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    attempts = 0
    status_code = 400

    while status_code >= 400 and attempts < 5:
        # print("[INFO] Retrieving data, attempt number: {}".format(attempts))
        req = requests.get(url=url, headers=headers)
        status_code = req.status_code
        attempts += 1
        time.sleep(1)
    if int(req.text.find("\"context\"")) == -1:
        print("[Warning] Light_Results: Nothing uploaded!")
        return
    Light_time_head = int(req.text.find("\"timestamp\"")) + 13
    Light_time_last = int(req.text.find("\"value\"")) - 2
    Light_value_head = int(req.text.find("\"value\"")) + 9
    Light_value_last = int(req.text.find("\"context\"")) - 2
    Light_img_head = int(req.text.find("\"context\"")) + 20
    Light_img_last = int(req.text.find("\"created_at\"")) - 4
    Light_img = base64.b64decode(req.text[Light_img_head:Light_img_last])
    with open("Light_img.jpg", "wb") as f:
        f.write(Light_img)
    print("[INFO] Light_Results:", "建立時間", TimeTrans(int(req.text[Light_time_head:Light_time_last])), ", 亮度",
          req.text[Light_value_head:Light_value_last])

    # print(req.text)


def get_Wind(url=ENDPOINT, device=DEVICE_LABEL, variable=VARIABLE_LABEL,
             token=TOKEN):
    variable = "wind"
    url = "http://{}/api/v1.6/devices/{}/{}/values/?page_size=2".format(url,
                                                                        device,
                                                                        variable)

    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    attempts = 0
    status_code = 400

    while status_code >= 400 and attempts < 5:
        # print("[INFO] Retrieving data, attempt number: {}".format(attempts))
        req = requests.get(url=url, headers=headers)
        status_code = req.status_code
        attempts += 1
        time.sleep(1)
    if int(req.text.find("\"context\"")) == -1:
        print("[Warning] Wind_Results: Nothing uploaded!")
        return
    Wind_time_head = int(req.text.find("\"timestamp\"")) + 13
    Wind_time_last = int(req.text.find("\"value\"")) - 2
    Wind_value_head = int(req.text.find("\"value\"")) + 9
    Wind_value_last = int(req.text.find("\"context\"")) - 2
    Wind_way_head = int(req.text.find("\"context\"")) + 20
    Wind_way_last = int(req.text.find("\"created_at\"")) - 4
    print("[INFO] Wind_Results: ", "建立時間", TimeTrans(int(req.text[Wind_time_head:Wind_time_last])), ", 風速",
          req.text[Wind_value_head:Wind_value_last], ", 風向", req.text[Wind_way_head:Wind_way_last])


def get_Rain(url=ENDPOINT, device=DEVICE_LABEL, variable=VARIABLE_LABEL,
             token=TOKEN):
    variable = "rain"
    url = "http://{}/api/v1.6/devices/{}/{}/values/?page_size=2".format(url,
                                                                        device,
                                                                        variable)

    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    attempts = 0
    status_code = 400

    while status_code >= 400 and attempts < 5:
        # print("[INFO] Retrieving data, attempt number: {}".format(attempts))
        req = requests.get(url=url, headers=headers)
        status_code = req.status_code
        attempts += 1
        time.sleep(1)

    if int(req.text.find("\"context\"")) == -1:
        print("[Warning] Rain_Results: Nothing uploaded!")
        return
    Rain_time_head = int(req.text.find("\"timestamp\"")) + 13
    Rain_time_last = int(req.text.find("\"value\"")) - 2
    Rain_value_head = int(req.text.find("\"value\"")) + 9
    Rain_value_last = int(req.text.find("\"context\"")) - 2
    Rain_state_head = int(req.text.find("\"context\"")) + 20
    Rain_state_last = int(req.text.find("\"created_at\"")) - 4
    print("[INFO] Rain_Results: ", "建立時間", TimeTrans(int(req.text[Rain_time_head:Rain_time_last])), ", 雨量階段",
          req.text[Rain_value_head:Rain_value_last], ", 對應雨量高度", req.text[Rain_state_head:Rain_state_last])


def get_var(url=ENDPOINT, device=DEVICE_LABEL, variable=VARIABLE_LABEL,
            token=TOKEN):
    try:
        get_Rain(url, device, variable, token)
        get_Wind(url, device, variable, token)
        get_Light(url, device, variable, token)
    except Exception as e:
        print("[ERROR] Error posting, details: {}".format(e))


if __name__ == "__main__":
    if TOKEN == "...":
        print("Error: replace the TOKEN string with your API Credentials.")
        sys.exit()
    while True:
        print("-----------------------------------------")
        get_var()

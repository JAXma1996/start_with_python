# -*- coding: utf-8 -*-
# utils.py (Python 3 version)
import json
import requests
from datetime import datetime, timedelta

# 全局请求头
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://www.yanlordlife.cn",
    "Referer": "http://www.yanlordlife.cn/stadium/booking/03681010-10c5-4fd5-a7fa-27532d1059dc",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
}

# 使用 Session 自动管理 Cookie
session = requests.Session()
session.headers.update(headers)

course_id_map = {
    "course_2": "52510dba-7e49-452f-93bf-588aad6c30ef",
    "course_3": "939fd40c-bb38-41dd-b74c-7618be7d45b0",
    "course_4": "a76ba330-dd43-4d9c-888c-3e1864c9acc8"
}

schedule_time_map = {
    "08": "2a2acc85-8aff-49fc-9e59-f4bd83cdfac8",
    "09": "de2b6e47-db54-4b02-9c42-4a9310da8ef7",
    "10": "fb0a41e8-eef4-4ae8-b526-3d25b9437589",
    "16": "2f0f0103-2518-4a18-b697-aa5597830bab",
    "17": "fdf9c97c-bdd4-44fb-9aac-41f2861c68e4",
    "18": "5d860220-f300-4815-9ef6-438b6c41ab40",
    "19": "03a3d24f-5052-467e-b431-25a06091d876",
    "20": "0cefc30c-7da4-418f-8ca7-f101bc05c8cb",
    "21": "10476590-4a7a-425c-879e-c14c8a5ae66c",
    "22": "60386a33-c47f-43fe-9dc4-074d8dd777aa"
}


def book_course(course_id, schedule, data_template):
    # 计算日期
    future_date = datetime.now().date() + timedelta(days=6)
    date_str = future_date.strftime('%Y-%m-%d')

    # 构建 payload
    payload = data_template.copy()
    payload["courtId"] = course_id_map[course_id]
    payload["bookingDate"] = date_str
    payload["schedules"] = [schedule_time_map[schedule]]

    try:
        # verify=False 跳过 SSL 验证 (对应原代码的 context)
        response = session.post(
            "http://www.yanlordlife.cn/api/front/club/venue/booking",
            json=payload,
            timeout=10,
            verify=False
        )

        response_data = response.json()
        code = response_data.get('code')
        message = response_data.get('message')

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"时间：{current_time} 场次：{course_id} 预定时间段：{schedule} "
              f"code：{code} message：{message}")

        # 业务逻辑映射
        if message in ["选择场次已被占用，不可以预订了", "工作日最多允许预定同一场馆2个场次"]:
            code = 22

        return code

    except requests.exceptions.RequestException as e:
        print(f"请求发生异常: {e}")
        return 'fail'


def login(username):
    login_url = 'http://www.yanlordlife.cn/api/front/member/login'
    payload = {"username": username, "password": "123456"}

    try:
        # 发送登录请求，session 会自动保存 Set-Cookie
        response = session.post(login_url, json=payload, verify=False)

        # 打印原始 Cookie 信息用于调试
        print("当前 Session Cookies:")
        for cookie in session.cookies:
            print(f"Name: {cookie.name}, Value: {cookie.value}")

        if 'connect.sid' in session.cookies.get_dict():
            print(f"\n登录成功，已获取 connect.sid: {session.cookies['connect.sid']}")
        else:
            print("\n登录失败或未找到 connect.sid")

    except Exception as e:
        print(f"登录发生错误: {str(e)}")

# 使用示例：
# login("your_username")
# book_course("course_2", "18", {})
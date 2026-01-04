# -*- coding: utf-8 -*-
# main.py (Python 3 version)
import time
from datetime import datetime
# 确保你已经按照我上一个回复修改了 util.py
from util import login, book_course, headers

# 预订基础配置
data = {
    "venueId": "03681010-10c5-4fd5-a7fa-27532d1059dc",
    "password": "960663"
}

# 目标时间段：晚上 20:00
schedule = "20"

# 场次开关逻辑
course_2_flag = False
course_3_flag = False
course_4_flag = True

# 执行登录获取 Session/Cookie
login("mahaibin")
print(f"当前请求头配置: {headers}")

# --- 1. 定时等待逻辑 ---
current_hour = datetime.now().hour
# 原逻辑：如果当前时间在凌晨 5 点之后，就一直等待直到进入 0-5 点区间
# 注意：如果是为了抢凌晨 6 点放的场，这里可能需要根据实际放票时间微调
while current_hour > 5:
    print(f"当前时间是 {datetime.now()}，尚未到预定执行时间（凌晨5点前），循环等待...")
    time.sleep(3)
    current_hour = datetime.now().hour

print("已进入执行预定时间段，准备启动...")
# 额外等待 15 秒（原代码逻辑）
time.sleep(15)

# --- 2. 抢票循环逻辑 ---
while True:
    # 尝试抢 2 号场
    if course_2_flag:
        code1 = book_course("course_2", schedule, data)
        if code1 == 0:
            print("场次 2 抢购成功！")
            break
        elif code1 == 22:
            print("场次 2 已被占用或达到上限，放弃该场次。")
            course_2_flag = False

    # 尝试抢 3 号场
    if course_3_flag:
        code2 = book_course("course_3", schedule, data)
        if code2 == 0:
            print("场次 3 抢购成功！")
            break
        elif code2 == 22:
            print("场次 3 已被占用或达到上限，放弃该场次。")
            course_3_flag = False

    # 尝试抢 4 号场
    if course_4_flag:
        code3 = book_course("course_4", schedule, data)
        if code3 == 0:
            print("场次 4 抢购成功！")
            break
        elif code3 == 22:
            print("场次 4 已被占用或达到上限，放弃该场次。")
            course_4_flag = False

    # 检查是否所有目标场次都失败了
    if not any([course_2_flag, course_3_flag, course_4_flag]):
        print("所有指定场次在该时间段均不可预订，停止执行。")
        break

    # 抢票频率控制（原代码为 2 秒）
    time.sleep(2)
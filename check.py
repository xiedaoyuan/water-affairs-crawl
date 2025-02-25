from playwright.sync_api import sync_playwright  
from sqlalchemy import create_engine, Column, String, DateTime  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker  
from datetime import datetime  
import json  

DATABASE_URL = 'postgresql://postgres:200364@localhost:5432/water'  
Base = declarative_base()  
   
# 数据库表模型，用于存储水资源相关信息  
class Water_Search(Base):  
    __tablename__ = 'waterwater'  
    title = Column(String, primary_key=True)  
    location = Column(String)  
    time = Column(DateTime)  
    link = Column(String)  
   
# 创建数据库连接  
engine = create_engine(DATABASE_URL)  
Base.metadata.create_all(engine)  # 创建表  
Session = sessionmaker(bind=engine)  
   
# 提取页面信息的函数  
def extract_information(page):  
    # 提取每一页的信息  
    titles = page.locator('td[id^="title"] a span[id^="onlytitle"]').all_text_contents()  
    locations = page.locator('td[id^="prov"]').all_text_contents()  
    times = page.locator('td[id^="pubdate"]').all_text_contents()  
    links = page.locator('td[id^="title"] a').evaluate_all('elements => elements.map(e => e.href)')  # 提取链接  

    # 将提取的信息组合成字典  
    return [{"title": title, "location": location, "time": time, "link": link}  
            for title, location, time, link in zip(titles, locations, times, links)]  
   
# 定义关键词列表  
keywords = [  
    "智慧水务", "智慧供水", "智慧排水", "智慧环保",  
    "城乡供水一体化","海绵城市智慧管控", "窨井水质检测",  
    "水站预警监控", "引水调度系统", "水利", "电厂", "锅炉水", "矿井水综合利用处理",  
    "高盐水处理", "油田注水后水质监测", "中水回用", "零排放", "零直排",
    "农饮水数字化", "加压泵站智慧化", "水泵房数字化", "智慧水厂", "供水数字化", "营收信息化",
    "水质监控系统", "智慧灌区","管网信息化", "管网地理信息管理", "排水监测信息化",
    "排水智慧监管", "管网漏损监测", "水质在线监测预警", "引水工程信息化","高盐水处理",
    "农污信息化", "城市排涝平台"  
]  
   
# 启动浏览器并进行搜索  
with sync_playwright() as p:  
    browser = p.chromium.launch(headless=False, channel='msedge')  
     
    all_information = []  # 用于存储所有页面的信息  
   
    for keyword in keywords:  
        page = browser.new_page()  
        page.goto("https://s.zhaobiao.cn/search/index")  
        page.wait_for_timeout(2000)  # 等待加载  
        page.get_by_role("textbox", name="搜索商机信息").click()  
        page.get_by_role("textbox", name="搜索商机信息").fill(keyword)  
        page.get_by_role("textbox", name="搜索商机信息").press("Enter")  
        page.wait_for_timeout(2000)  # 等待加载  
        page.get_by_role("link", name="准确搜索").click()  
        page.wait_for_timeout(2000)  # 等待加载  
   
        last_page_information = []  # 用于存储上一页的信息  
        for page_number in range(1, 51):  # 假设你想翻50页  
            # 提取当前页面的信息  
            page_information = extract_information(page)  
            # 输出当前页提取的信息数量  
            print(f"关键词 '{keyword}' - 提取第 {page_number} 页的信息数量: {len(page_information)}")  
   
            all_information.extend(page_information)  # 将当前页的信息添加到总列表中  
   
            # 检查是否满足跳出循环的条件  
            if len(page_information) < 50 and page_information == last_page_information:  
                print(f"关键词 '{keyword}' - 信息数量不足50且与上一页相同，结束提取。")  
                break  

            last_page_information = page_information  # 更新上一页的信息  
            
            # 点击下一页  
            try:  
                next_button = page.get_by_role("link", name="下一页")  
                if next_button.is_visible():  # 检查下一页按钮是否可见  
                    next_button.click()  
                    page.wait_for_timeout(1000)  # 等待加载新页面  
                else:  
                    print(f"关键词 '{keyword}' - 已经到达最后一页，第 {page_number} 页结束。")  
                    break  # 如果没有找到下一页，跳出循环  
            except Exception as e:  
                print(f"关键词 '{keyword}' - 无法找到下一页链接: {e}")  
                break  # 如果没有找到下一页，跳出循环  
         
        # 创建数据库会话并插入数据  
        session = Session()  
        for info in all_information:  
            try:  
                formatted_time = datetime.strptime(info['time'], "%Y-%m-%d")  # 转换时间格式  
                # 检查是否已存在相同的 title  
                existing_offer = session.query(Water_Search).filter_by(title=info['title']).first()  
                if existing_offer is None:  
                    waterwater = Water_Search(  
                        title=info['title'],  
                        location=info['location'],  
                        time=formatted_time,  
                        link=info['link']  
                    )  
                    session.add(waterwater)  
                else:  
                    print(f"记录已存在: {info['title']}")  # 输出已存在的记录  
            except Exception as e:  
                print(f"插入记录时出错: {e}")  
        # 关闭当前页  
        page.close()  
        session.commit()  # 提交数据  
        session.close()  # 关闭会话  
   
    # 打印或保存提取的信息  
    print(f"共提取到 {len(all_information)} 条信息：")  
    for info in all_information:  
        print(info)  
   
    browser.close()
    
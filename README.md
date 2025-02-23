**项目简介**：这个项目旨在使用 Playwright 和 SQLAlchemy 从指定网站抓取与水务相关的信息，并将其存储到 PostgreSQL 数据库中。
             它能够根据给定的关键词进行搜索，提取相关信息，并处理多页结果。并且通过 Node.js 和 Express ，提供一个搜索接口，
             用于从 PostgreSQL 数据库中检索与水务相关的信息。用户可以通过在网页上通过关键词搜索，获取相关的记录。
             

**功能**：使用 Playwright 自动化浏览器进行网页抓取。  
          提取标题、位置、时间和链接等信息。  
          将抓取的数据存储到 PostgreSQL 数据库中。  
          支持多个关键词的搜索。
          可以在网页上对对数据库进行关键词搜索


**安装**： Python 3.7+, PostgreSQL 数据库,  Node.js (建议使用 LTS 版本), npm


**安装库**：pip install playwright sqlalchemy psycopg2
           npm install express body-parser cors dotenv pg


**使用说明**：首先通过crawl666.py和crawl777.py对数据进行爬取和保存，其中DATABASE_URL = 'postgresql://postgres:200364@localhost:5432/water'
              需要换成你自己的postgresql的数据库格式'postgresql://用户名:密码@localhost:端口号/数据库名称'
              class Water_Search(Base):中__tablename__ = 'waterwater'换成你的数据库中的表格名称，
              之后通过命令台输入指令，到你保存的文件夹下，输入npm start，它会生成一个链接 http://localhost:3000，
              点击这个链接就可以进入信息界面，可以通过关键词对爬取到的信息进行检索。      


**联系方式**：xiedaoyuan0364@outlook.com  

import pymysql

conn = pymysql.connect(host='localhost', user='root', password='admin',charset='utf8',database='scraping',
                             cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute('USE scraping')
cur.execute('SELECT * FROM pages')
print(cur.fetchone())
cur.close()
conn.close()
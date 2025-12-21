# test file to figure out if the databse is successfully connected or not
import pymysql

try:
    conn = pymysql.connect(
        host="127.0.0.1",
        user="root",
        password="Aw2p2df23_dz!io.",
        database="nu_volunteering_hub",
        port=3306
    )
    print("✅ Connected to MySQL database successfully!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)

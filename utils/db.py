from pymysql import Connection
import pymysql

# ... 这里保留你上面的 getCon 和 closeCon 函数定义 ...

def getCon():
    """
    获取数据连接
    """
    con = Connection(
        host="localhost",
        port=3306,
        user="root",
        password="123456",  # 确保这里是你刚才重置的新密码
        database="ycrp",    # 如果报错 Unknown database，说明DataGrip里没建这个库
        autocommit=True
    )
    return con

def closeCon(con: Connection):
    if con:
        con.close()

# === 下面是测试代码 ===
if __name__ == '__main__':
    print("正在尝试连接数据库...")
    try:
        # 1. 尝试获取连接
        conn = getCon()
        print("✅ 连接对象创建成功！")
        
        # 2. 执行一个简单的查询来验证真的通了
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ 数据库交互成功！当前 MySQL 版本: {version[0]}")
            
            # 可选：查看当前库里有哪些表，确认 ycrp.sql 导入没
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            print(f"📄 当前库({conn.db.decode()}) 中的表: {tables}")

        # 3. 关闭连接
        closeCon(conn)
        print("连接已安全关闭。")

    except pymysql.err.OperationalError as e:
        code, message = e.args
        if code == 1049:
            print(f"❌ 错误：找不到数据库 'ycrp'。")
            print("💡 解决办法：请回到 DataGrip，先创建名为 ycrp 的数据库，或者运行 SQL 文件。")
        elif code == 1045:
            print(f"❌ 错误：密码或用户名错误。")
            print("💡 解决办法：请检查代码里的 password 字段是否是 '123456'。")
        else:
            print(f"❌ 连接错误: {e}")
    except Exception as e:
        print(f"❌ 发生了其他错误: {e}")
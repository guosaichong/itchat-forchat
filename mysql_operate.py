import pymysql


def computer_query(sql):
    conn=pymysql.Connect(host='47.105.166.136',port=3306,user='test',passwd='123456',db='yufan',charset='utf8')
    cur = conn.cursor()
    
    cur.execute(sql)
    u = cur.fetchall()

    print(u)
    cur.close()
    conn.close()
    return u
    
if __name__ =="__main__":
    sql="select * from computer_info;"
    computer_query(sql)
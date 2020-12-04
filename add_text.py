import pymysql


def add_text(char):
    conn = pymysql.Connect(host='47.105.166.136', port=3306,
                           user='test', passwd='123456', db='dictionary', charset='utf8')
    cur = conn.cursor()
    value=(char)
    sql = "insert into chinese(sentence)values(%s)" 
    cur.execute(sql,value)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    char = "强者遇到强者，只会暗中比较；但弱者遇到强者，除了嘴上叫嚣，别的什么也做不了"
    add_text(char)

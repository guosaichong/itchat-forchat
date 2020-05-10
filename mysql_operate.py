import pymysql
from youdao import get_data

def delete_word(char):
    try:
        conn=pymysql.Connect(host='47.105.166.136',port=3306,user='test',passwd='123456',db='dictionary',charset='utf8')
        cur = conn.cursor()
        cur.execute("select word from english where word='{}' limit 1;".format(char))
        u = cur.fetchone()
        # print(u)
        if u == None:
            print("{}不存在,删除失败！".format(char))
        else:
            select = "delete FROM english WHERE word='{}';".format(char)
            cur.execute(select)
            conn.commit()
            print("已删除")
        cur.close()
        conn.close()
    except Exception as e:
        print(e)
        print("删除失败！")
def add_word(char):
    conn=pymysql.Connect(host='47.105.166.136',port=3306,user='test',passwd='123456',db='dictionary',charset='utf8')
    cur = conn.cursor()
    cur.execute("select * from english where word='%s' limit 1;"%char)
    u = cur.fetchone()
    if u == None:
        paraph=get_data(char)
        word=paraph[0]
        IPA=paraph[1]
        paraphrase=paraph[2]
        example_sentence=paraph[3]+paraph[4]
        other=paraph[5]
        value=(word,IPA,paraphrase,example_sentence,other)
        sql="insert into english(word,IPA,paraphrase,example_sentence,other)values(%s,%s,%s,%s,%s)"
        cur.execute(sql,value)
        conn.commit()
        print("已添加")
        print(word+'\n'+IPA+'\n'+paraphrase+'\n'+example_sentence+'\n'+other)
    else:
        print(u[1]+'\n'+u[2]+'\n'+u[3]+'\n'+u[4]+'\n'+u[5])
    
    cur.close()
    conn.close()
    
if __name__ =="__main__":
    # delete_word("model")
    add_word("model")
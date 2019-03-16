import json
import redis
import pymysql


def main():
    rediscli = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
    mysqlcli = pymysql.connect(host='127.0.0.1', user='root', passwd='root',
                               db='redis_info', port=3306, use_unicode=True)
    while True:
        # FIFO模式为 blpop，LIFO模式为 brpop，获取键值
        source, data = rediscli.blpop(["fang:items"])
        item = json.loads(data)

        try:
            # 使用cursor()方法获取操作游标
            cur = mysqlcli.cursor()
            # 使用execute方法执行SQL INSERT语句
            cur.execute(
                "INSERT INTO data1 (house_name, address, district, house_type, area, price,  house_url, labels,onsale) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s )",
                [item['house_name'], item['address'], item['district'], item['house_type'], item['area'], item['price'],
                 item['house_url'], item['labels'], item['onsale']])
            # 提交sql事务
            mysqlcli.commit()
            # 关闭本次操作
            cur.close()
        except Exception as e:
            print(e)
            print("Mysql Error:\n%s" % item)

if __name__ == '__main__':
    main()

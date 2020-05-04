# send$request transaction date -> timestemp
# change Name column of UserAccount -> UName

import pymysql
import pandas as pd
from datetime import datetime
from statistics import mean

# 加入debug功能
pymysql.install_as_MySQLdb()
pymysql.connections.DEBUG = True

# 打开数据库连接
db = pymysql.connect(host = "localhost",user = "root", password = "Lizy52391?", db = "cs631Pro", port = 3306)

# 使用cursor()方法获取操作游标
cursor = db.cursor()

############################################# Main Menu #####################################################
# 注册账号
def signup(bankid,banknum,verify,SSN,username,email):
    # SQL 插入BankAccount
    sql1 = """INSERT INTO BankAccount(BankID, \
           BANumber, Verified) \
           VALUES (%s,  %s,  %s)""" % \
           (bankid,banknum,verify)

    # SQL 插入UserAccount
    sql2 = """INSERT INTO UserAccount(SSN,
              UName, PBankID, PBANumber)
             VALUES (%s,'%s', %s, %s)""" %\
           (SSN,username,bankid,banknum)

    # SQL 插入ElectronicAddress
    sql3 = """INSERT INTO ElectronicAddress(Identifier)
             VALUES ('%s')""" %\
           (email)

    # SQL 插入EmailAddress
    sql4 =  """INSERT INTO EmailAddress(Identifier,
              Verified,USSN)
             VALUES ('%s', %s, %s)""" %\
           (email,verify,SSN)

    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.execute(sql3)
        cursor.execute(sql4)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 实现登陆功能
def login(UserName,SSN):
    # SQL 搜索UserAccount
    sql = """SELECT * FROM UserAccount
            WHERE SSN = %s
             """ %\
          (SSN)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('Error: unable to fetch data')
################### 搜寻结果 ################### 若数据库变动 以下索引也将改变
    for row in results:
        USSN = row[0]
        UName = row[1]
        UBalance = row[2]
        UBankID = row[3]
        UBankNum = row[4]
    if UName == UserName:
        print("USSN: %d, UName: %s, UBalance: %s ,UBankID: %s ,UBankNum: %s " % (USSN,UName,UBalance,UBankID,UBankNum))
    else:
        print('UserName Error')



# 实现付款功能
def send(transamount,memo,cancled,SSN,to_email,istonew):
    # SQL 插入SendTransaction
    sql = """INSERT INTO SendTransaction(Amount,
              Memo, Cancelled, ISSN, ToIdentifier,IsToNewUser)
             VALUES (%s,'%s', %s, %s,'%s',%s)""" %\
           (transamount,memo,cancled,SSN,to_email,istonew)

    try:
        # 执行sql语句
        cursor.execute(sql)
        cursor.execute
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 实现收款功能
def request(requestamount,memo,mySSN,targetemail):
# SQL 插入RequestTransaction
    sql1 = """INSERT INTO RequestTransaction(TotalAmount,
              Memo, ISSN)
             VALUES (%s,'%s', %s)""" %\
           (requestamount,memo,mySSN)
# SQL 插入RequestFrom
    sql2 = """INSERT INTO RequestFrom(Amount,
              EIdentifier)
             VALUES (%s,'%s')""" %\
            (requestamount,targetemail)
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.commit()
    except:
        db.rollback()
        print('ERROR')

# 搜索发送交易信息
def searchsend_byEmail(SSN,targetemail):
    if targetemail is not None:
        # SQL 查询语句
        sql = "SELECT * FROM SendTransaction \
               WHERE ISSN = %s AND ToIdentifier = '%s'" % (SSN,targetemail)
    else:
        # SQL 查询语句
        sql = "SELECT * FROM SendTransaction \
               WHERE ISSN = %s " % (SSN)
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 获取所有记录列表
       results = cursor.fetchall()
       for row in results:
        print(row)
    except:
        print('Error: unable to fetch data')

############################################# Account Function #####################################################
## 修改个人信息
# 更改用户名
def changename(SSN,NewName):
    # SQL 更新UserAccount
    sql = """UPDATE UserAccount SET UName = '%s' WHERE SSN = %s """ %\
          (NewName,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 添加邮箱
def addemail(newemail,SSN,verify):
    # SQL 插入SendTransaction
    sql1 = """INSERT INTO ElectronicAddress(Identifier)
             VALUES ('%s')""" %\
           (newemail)
    sql2 = """INSERT INTO EmailAddress(Identifier,
              Verified, USSN)
             VALUES ('%s', %s, %s)""" %\
           (newemail,verify,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 删除邮箱
def removemail(newemail,SSN):
    # SQL 删除目标行
    sql1 = """DELETE FROM ElectronicAddress
            WHERE Identifier = '%s' """ %\
           (newemail)
    sql2 = """DELETE FROM EmailAddress
              WHERE Identifier = '%s' AND USSN = '%s' """ %\
           (newemail,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 添加电话号
def addphone(newphone,SSN,verify):
    # SQL 插入SendTransaction
    sql1 = """INSERT INTO ElectronicAddress(Identifier)
             VALUES ('%s')""" %\
           (newphone)
    sql2 = """INSERT INTO Phone(Identifier,
              Verified, USSN)
             VALUES ('%s', %s, %s)""" %\
           (newphone,verify,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 删除电话号
def removephone(newphone,SSN):
    # SQL 删除目标行
    sql1 = """DELETE FROM ElectronicAddress
            WHERE Identifier = '%s' """ %\
           (newphone)
    sql2 = """DELETE FROM Phone
              WHERE Identifier = '%s' AND USSN = '%s' """ %\
           (newphone,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 添加银行信息（银行账户是否已经存在BankAccount？）
def addbank(BankId,BankNum,SSN,verify):
    # SQL 插入BankAccount
    sql1 = """INSERT INTO BankAccount(BankId,BANumber,Verified)
             VALUES (%s,%s,%s)""" %\
           (BankId,BankNum,verify)
    # SQL 插入Has_Additional
    sql2 = """INSERT INTO Has_Additional(UBankId,UBANumber,USSN)
             VALUES (%s,%s,%s)""" %\
           (BankId,BankNum,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql1)
        cursor.execute(sql2)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

# 删除银行信息 (未删除BankAccount里信息）
def removebank(BankId,BankNum,SSN):
    # SQL 删除Has_Additional
    sql1 = """DELETE FROM Has_Additional
              WHERE UbankID = %s AND UBANumber = %s and USSN = %s """ %\
           (BankId,BankNum,SSN)
    try:
        # 执行sql语句
        cursor.execute(sql1)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('ERROR')

############################################# Statement Function #####################################################
# 搜索发送交易
def searchSend_byDate(SSN,startdate,tilldate): # 输入的日期为'string', Example: '2019-02-03' or '2019/04/05'
    # 将输入的日期转化
    start =  pd.to_datetime(startdate)
    end = pd.to_datetime(tilldate)
    # 搜索SendTransaction
    sql = """SELECT * FROM SendTransaction
            WHERE ISSN = %s
             """ % \
          (SSN)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('Error: unable to fetch data')
    # 筛选日期
    TotalAmount = 0
    for row in results:
        pddate = pd.to_datetime(row[2])
        if pddate < end:
            if pddate > start:
                TotalAmount += row[1]
                print(row)
    return TotalAmount

# 搜索收取信息
def searchRequest_byDate(SSN,startdate,tilldate): # 输入的日期为'string', Example: '2019-02-03' or '2019/04/05'
    # 将输入的日期转化
    start =  pd.to_datetime(startdate)
    end = pd.to_datetime(tilldate)
    # 搜索SendTransaction
    sql = """SELECT * FROM RequestTransaction
            WHERE ISSN = %s
             """ % \
          (SSN)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('Error: unable to fetch data')
    # 筛选日期
    TotalAmount = 0
    for row in results:
        pddate = pd.to_datetime(row[2])
        if pddate < end:
            if pddate > start:
                TotalAmount += row[1]
                print(row)
    return TotalAmount

# 返回每月消费总量 以及月消费平均值
def searchTotalAverage(SSN):
    # 搜索SendTransaction
    sql = """SELECT * FROM SendTransaction
            WHERE ISSN = %s
             """ % \
          (SSN)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('Error: unable to fetch data')
    # 建立哈希表记录月份信息
    SendMonth = {}
    for row in results:
        date = datetime.strftime(row[2],'%Y-%m')
        # print(row)
        if date not in SendMonth:
            SendMonth[date] = [row[1]]
        else:
            SendMonth.get(date).append(row[1])

    # 搜索SendTransaction
    sql = """SELECT * FROM RequestTransaction
            WHERE ISSN = %s
             """ % \
          (SSN)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
    except:
        # 如果发生错误则回滚
        db.rollback()
        print('Error: unable to fetch data')
    # 建立哈希表记录月份信息
    RequstMonth = {}
    for row in results:
        date = datetime.strftime(row[2],'%Y-%m')
        # print(row)
        if date not in RequstMonth:
            RequstMonth[date] = [row[1]]
        else:
            RequstMonth.get(date).append(row[1])
    # 计算月份均值 总量 最大值
    for key in SendMonth:
        total = sum(SendMonth.get(key))
        average = mean(SendMonth.get(key))
        Maximum = max(SendMonth.get(key))
        print('月份: %s, 付款总量: %d, 付款均值: %d, 当月最大付款: %d' %(key,total,average,Maximum))
    for key in RequstMonth:
        total = sum(RequstMonth.get(key))
        average = mean(RequstMonth.get(key))
        Maximum = max(RequstMonth.get(key))
        print('月份: %s, 收款总量: %d, 收款均值: %d, 当月最大收款: %d' %(key,total,average,Maximum))

# 搜索最佳使用者
def bestuser():
    # SQL 查询语句
    sql1 = """select sum(TotalAmount),U.SSN, UName
            from RequestTransaction R, UserAccount U 
            where R.ISSN = U.SSN
            group by U.SSN, UName 
            """
    sql2 = """select sum(Amount),U.SSN, UName
            from SendTransaction S, UserAccount U 
            where S.ISSN = U.SSN
            group by U.SSN, UName 
            """
    try:
        # 执行SQL语句
        cursor.execute(sql1)
        # 获取所有记录列表
        results1 = cursor.fetchall()
        cursor.execute(sql2)
        results2 = cursor.fetchall()
        record = {}
        for row in results1:
            record[row[1]] = row[0]
        for row in results2:
            if row[1] not in record:
                record[row[1]] = row[0]
            else:
                record[row[1]] += row[0]
        maxi = [0,0]
        for key in record:
            if record.get(key) > maxi[1]:
                maxi[1] = record.get(key)
                maxi[0] = key
        print(maxi)
    except:
        print('Error: unable to fetch data')








# login('lizy',641)
# signup(1314,520,1,641,'lizy','zl489@njit.edu')
# request(450,'dinner',641,'minna_amigon@yahoo.com')
# send(200,'hot',0,641,'yuki_whobrey@aol.com',0)
# searchsend_byEmail(172,'lexter@dexter.com')
# addemail('lizy.li@valpo.edu',641,1)
# removemail('lizy.li@valpo.edu',641)
# addphone(55555555,641,1)
# removephone(55555555,641)
# addbank(11111,11111,172,1)
# removebank(8802847,11111,641)
# changename(641,'Lizy331')
# test_searchSend = searchSend_byDate(641,'2020/5/2','2020/5/3')
# print(test_searchSend)
# test_searchRequest = searchRequest_byDate(172,'2018-12-9','2018-12-20')
# print(test_searchRequest)
# searchTotalAverage(172)
bestuser()


# 关闭数据库连接
db.close()
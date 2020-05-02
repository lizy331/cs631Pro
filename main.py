# send$request transaction date -> timestemp
# change Name column of UserAccount -> UName

import pymysql

# 加入debug功能
pymysql.install_as_MySQLdb()
pymysql.connections.DEBUG = True

# 打开数据库连接
db = pymysql.connect(host = "localhost",user = "root", password = "密码", db = "cs631Pro", port = 3306)

# 使用cursor()方法获取操作游标
cursor = db.cursor()

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
def searchsend(SSN,targetemail):
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

signup(1314,520,1,641,'lizy','zl489@njit.edu')
request(450,'dinner',641,'minna_amigon@yahoo.com')
send(127,'hospital',0,641,'yuki_whobrey@aol.com',0)
searchsend(172,'lexter@dexter.com')
# 关闭数据库连接
db.close()

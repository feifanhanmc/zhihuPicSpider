# -*- coding: utf-8 -*-
import MySQLdb

class Database:
    '''
        目前仅支持字符类型str的数据操作。
    '''
    def __init__(self, dbname, host="localhost", user="root", pwd="root", charset="utf8"):
        self.dbname = dbname
        self.host = host
        self.user = user
        self.pwd = pwd
        self.charset = charset
    
    def connect(self):
        db = MySQLdb.connect(self.host, self.user, self.pwd, self.dbname)
        db.set_character_set(self.charset)
        return db
        
    def create_table(self, table_name,  sql):
        '''
        :param table_name(str) 、 sql(str)
        '''
        db = self.connect()
        cursor = db.cursor()
        cursor.execute('DROP TABLE IF EXISTS ' + table_name)
        try:
            cursor.execute(sql)
            print '创建数据表' + table_name + '成功'
        except Exception,e:
            print '创建数据表' + table_name + '失败'
            print '错误原因  : ',e
        db.close()  
    
    def save_data(self, table_name, data_headers, data):
        '''
        :param data_headers(list of data_name(str)) 、 data(list of list)
        for example:
            data_headers = ['username', 'pwd']
            data = [['hmc', '123'],
                    ['admin', 'admin'],
                    ['root', 'root']] 
        '''
        db = self.connect()
        cursor = db.cursor()
        columc_num = len(data_headers)
        
        #拼接sqli语句
        sqli = 'INSERT INTO ' + table_name + '('
        datatype = '('
        for i in range(columc_num):
            if not i:
                sqli = sqli + data_headers[i]
                datatype += '%s'
            else:
                sqli = sqli + ', '  + data_headers[i]
                datatype += ', %s' 
        datatype += ')'
        sqli = sqli + ')' + ' VALUES ' + datatype
        
        #存储数据
        flag = True
        for d in data:
            t = []
            for i in range(columc_num):
                t.append(d[i])
            try:
                cursor.execute(sqli, tuple(t))
                db.commit()
            except Exception,e :
                print '存储失败，错误原因 :', e
                flag = False
                db.rollback()
        if flag:
            print '存储成功，共存储' + str(len(data)) + '条数据'
        db.close()
            
    
    def select(self, table_name, items='*'):
        '''
        :param items(str or list of str)。items为空则默认是所有表中的属性。
        '''
        db = self.connect()
        cursor = db.cursor()
        
        #拼接sql语句
        if isinstance(items, (list,tuple)):
            sql = 'SELECT '
            for i in range(len(items)):
                if not i :
                    sql = sql + items[i]
                else : 
                    sql = sql + ',' + items[i] 
            sql = sql + ' FROM ' + table_name
        elif isinstance(items, str):
            sql = 'SELECT ' + items + ' FROM ' + table_name
        else:
            sql = 'SELECT * FROM ' + table_name
        
        #数据库查询
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            print '查询成功'
        except Exception,e:
            print '查询失败，错误原因  : ', e
            db.rollback()
        db.close()
        return results
    
    def raw_select(self, sql):
        db = self.connect()
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            results = cursor.fetchall()
#             print '执行sql语句成功'
        except Exception,e :
            print '执行sql语句失败，错误原因 : ', e
            db.rollback()
        db.close() 
        return results
    
    def execute(self, sql):
        db = self.connect()
        cursor = db.cursor()
        flag = False
        try:
            cursor.execute(sql)
            db.commit()
#             print '执行sql语句成功'
            flag = True
        except Exception,e :
            print '执行sql语句失败，错误原因 : ', e
            db.rollback()
        db.close()
        if flag:
            return True
        else:
            return False

"""
if __name__ == "__main__":
    db = Database('mytest')
    sql = '''CREATE TABLE TEST(
    USER VARCHAR(10) PRIMARY KEY,
    PWD VARCHAR(10))
    '''
#     db.create_table('test', sql)
#     db.save_data('test', ['user', 'pwd'], [['hmc','123'],['root','toot']])
#     print db.select('test')
#     db.execute("DELETE FROM TEST WHERE USER = 'ROOT'")
"""
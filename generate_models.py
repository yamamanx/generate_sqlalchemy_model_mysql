# -*- coding: utf-8 -*-

import pymysql
import config
import logging.config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_type(type_str):
    sta = type_str.find('(')
    end = type_str.find(')')
    ts = type_str[0:3]
    length = -1
    unsigned = ''
    ret_type = ''

    if sta > 0:
        length = type_str[sta+1:end]
    if type_str.find('unsigned') > -1:
        unsigned = 'unsigned=True'

    if type_str.find('decimal') > -1:
        ret_type = 'DECIMAL()'
    elif type_str.find('bigint') > -1:
        ret_type = 'BIGINT(' + unsigned + ')'
    elif type_str.find('varchar') > -1:
        ret_type = 'VARCHAR(' + str(length) + ')'
    elif type_str.find('datetime') > -1:
        ret_type = 'DATETIME()'
    elif type_str.find('char') > -1:
        ret_type = 'CHAR(' + str(length) + ')'
    elif type_str.find('text') > -1:
        ret_type = 'TEXT()'
    elif type_str.find('tinyint') > -1:
        ret_type = 'TINYINT(' + unsigned + ')'
    elif type_str.find('time') > -1:
        ret_type = 'TIME()'
    elif type_str.find('int') > -1:
        ret_type = 'INTEGER(' + unsigned + ')'
    return ret_type


def generate_model(host,user,password,db_name):

    conn = pymysql.connect(
        host,
        user=user,
        passwd=password,
        db=db_name,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

    cur = conn.cursor()
    sql = 'show tables'
    cur.execute(sql)
    tables = cur.fetchall()

    write_file = open(db_name + '_models.txt', 'w')

    for table in tables:
        table_name = table['Tables_in_' + db_name]
        sql = 'show columns from ' + table_name
        cur.execute(sql)
        columns = cur.fetchall()
        write_file.write('\n\n')
        write_file.write('class ' + table_name.upper() + '(Base):\n')
        write_file.write("    __tablename__ = '" + table_name.upper() + "'\n\n")

        for column in columns:
            field_str = column['Field']
            type_str = column['Type']
            null_str = column['Null']
            key_str = column['Key']
            pri_str = ''
            null_able = ''
            if key_str == 'PRI':
                pri_str = ' primary_key=True, '
            if null_str == 'NO':
                null_able = 'nullable=False)'
            else:
                null_able = 'nullable=True)'

            line_str = '    '
            line_str += field_str + ' = Column('
            line_str += get_type(type_str) + ', '
            line_str += pri_str
            line_str += null_able

            write_file.write(line_str + '\n')

    write_file.close()

def main():
    host  = config.db_host
    user = config.db_username
    password = config.db_password
    db_name = config.db_name

    generate_model(host, user, password, db_name)

if __name__ == '__main__':
    logging.config.fileConfig("../logging.conf")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    event = {}
    main()

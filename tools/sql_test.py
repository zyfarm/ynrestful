from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, select

__author__ = 'jiyue'

class MetaDBConfig(object):
    db_name='db_dig_keys'
    db_user='admin'
    db_password='admin'
    db_host='localhost'

    @staticmethod
    def parseConfigDBUrl():
        return "mysql://"+MetaDBConfig.db_user+":"+MetaDBConfig.db_password+"@"+MetaDBConfig.db_host+"/"+MetaDBConfig.db_name





def main_entry():
    eng=create_engine(MetaDBConfig.parseConfigDBUrl())
    with eng.connect() as con:

        meta=MetaData(eng)

        metapoints=Table('ld_keys_metapoint',meta,autoload=True)

        stm=select([metapoints.c.description])
        rs=con.execute(stm)

        print rs.fetchone()





if __name__=='__main__':
    main_entry()
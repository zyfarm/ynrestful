# –*- encoding:utf8 –*-

from project.config.utils import ConfigInitor
from sqlalchemy import Integer, Column, String, DateTime, BigInteger, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

__author__ = 'jiyue'

Base = declarative_base()


class LDKeysMetapoint(Base):
    __tablename__ = 'ld_keys_metapoint'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    gmt_create = Column(DateTime)
    creator_id = Column(Integer)
    gmt_modified = Column(DateTime)
    modifier_id = Column(Integer)
    is_deleted = Column(Integer)
    category_id = Column(Integer)
    ref_count = Column(Integer)


class LDKeysRelation(Base):
    __tablename__ = 'ld_keys_relation'
    id = Column(BigInteger, primary_key=True)
    widget_id = Column(BigInteger)
    parent_widget_id = Column(BigInteger)
    is_delete = Column(SmallInteger)
    is_leaf = Column(SmallInteger)
    level = Column(Integer)
    restriction = Column(String)
    modifier_id = Column(BigInteger)
    creator_id = Column(BigInteger)
    gmt_modified = Column(DateTime)
    gmt_create = Column(DateTime)
    options = Column(String)
    model_version_id = Column(BigInteger)


class LDKeysWidget(Base):
    __tablename__ = 'ld_keys_widget'
    widget_id = Column(BigInteger, primary_key=True)
    path = Column(String)
    tpl = Column(String)
    is_repeatable = Column(SmallInteger)
    alias = Column(String)
    key_id = Column(BigInteger)
    gmt_create = Column(DateTime)
    gmt_modified = Column(DateTime)
    creator_id = Column(BigInteger)
    modifier_id = Column(BigInteger)


class LdKeysModel(Base):
    __tablename__ = 'ld_keys_model'
    id = Column(BigInteger, primary_key=True)
    model_id = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    hospital = Column(String)
    disease = Column(String)
    type = Column(SmallInteger)
    extra = Column(String)
    model_name = Column(String)
    status = Column(SmallInteger)


class LDKeysDBProxy(object):
    def __init__(self, engine):
        self.engine = engine
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        Base.metadata.create_all(self.engine)

    '''查询'''

    def query_for_all_data(self, model):
        data = self.session.query(model).all()
        return data

    # TODO 查询时要加入版本号的概念
    def query_for_desc_by_key(self, dt, key, hospital='standard', disease='model'):
        res = []
        data = self.session.query(LdKeysModel).filter(LdKeysModel.disease == disease).filter(
            LdKeysModel.hospital == hospital).one()
        keyAttr = key.split('|')
        resRoot = self.session.execute("select a.widget_id,a.key_id,a.path,a.alias,b.parent_widget_id "
                                       "from ld_keys_widget a "
                                       "inner join ld_keys_relation b "
                                       "on a.widget_id=b.widget_id "
                                       "where b.model_version_id=:model_id and a.path=:path",
                                       {'model_id': data.id,
                                        'path': keyAttr[0],
                                        'parent_widget_id': -1}).fetchone();

        if resRoot is None:
            return None;

        res.append(resRoot['alias'])
        for path in keyAttr[1:]:
            parent_id = resRoot['widget_id']
            resRoot = self.session.execute("select a.alias,a.widget_id,a.key_id from ld_keys_widget a "
                                           "inner join  ld_keys_relation b "
                                           "on a.widget_id=b.widget_id  "
                                           "where b.parent_widget_id=:parent_id and a.path=:path and b.model_version_id=:model_id",
                                           {'model_id': data.id, 'path': path, 'parent_id': parent_id}
                                           ).fetchone();
            if resRoot is None:
                return None

        if -1 == resRoot.key_id:
            return resRoot.alias, resRoot.key_id
        else:
            datapoint = self.query_for_metapoint_detail(resRoot['key_id'])
        return datapoint.description, datapoint.id

    def query_for_metapoint_detail(self, mid):
        data = self.session.query(LDKeysMetapoint).filter(LDKeysMetapoint.id == mid).one()
        return data

    def query_for_relation_all(self, hospital, disease, level):
        model_data = self.session.query(LdKeysModel).filter(LdKeysModel.hospital == hospital,
                                                            LdKeysModel.disease == disease).one()
        data = self.session.query(LDKeysRelation).filter(LDKeysRelation.model_version_id == model_data.id,
                                                         LDKeysRelation.level == level).all()
        return data

    def query_for_relation_parent_detail(self, hospital, disease, parent_widget_id):
        model_data = self.session.query(LdKeysModel).filter(LdKeysModel.hospital == hospital,
                                                            LdKeysModel.disease == disease).one()
        data = self.session.query(LDKeysRelation).filter(LDKeysRelation.model_version_id == model_data.id,
                                                         LDKeysRelation.parent_widget_id == parent_widget_id)
        return data

    def query_for_widget_detail(self, widget_id):
        data = self.session.query(LDKeysWidget).filter(LDKeysWidget.widget_id == widget_id).one()
        return data

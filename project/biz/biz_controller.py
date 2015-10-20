import json
import logging
import falcon
import jsonpickle
from project.config.utils import ConfigInitor
from project.decorators.wrapper_response import ApiDecorator
from project.models.proxy import LDKeysDBProxy, LDKeysMetapoint
from project.utils.mix_tools import sql_alchemy_to_json_encoder
from project.utils.relation import RelationNode
from project.utils.stack import Stack

__author__ = 'jiyue'


class MetaPointsController:
    def __init__(self):
        self.query_proxy = LDKeysDBProxy(ConfigInitor.db_engine)
        self.logger = logging.getLogger('main.biz')

    @ApiDecorator.sql_alchemy_json_serilizer([])
    def get_all_metapoints(self, rid):
        return self.query_proxy.query_for_all_data(LDKeysMetapoint)

    @ApiDecorator.sql_alchemy_json_serilizer([])
    def get_specific_metapoint(self, rid, mid=None):
        return self.query_proxy.query_for_metapoint_detail(mid)


class WidgetController:
    def __init__(self):
        self.query_proxy = LDKeysDBProxy(ConfigInitor.db_engine)
        self.logger = logging.getLogger('main.biz')

    def get_specific_widget(self, rid, wid):
        return self.query_proxy.query_for_widget_detail(wid)


class DataModelController(object):
    def __init__(self):
        self.query_proxy = LDKeysDBProxy(ConfigInitor.db_engine)
        self.logger = logging.getLogger('main.biz')

    def get_specific_disease_model(self, rid, dt, hospital, disease, formated='common'):
        self.logger.info("get_specific_disease_model rid: %s,dt: %s,hospital: %s,disease: %s",
                         [rid, dt, hospital, disease])
        if 'common' == formated:
            return compute_tree(self.query_proxy, hospital, disease)
        else:
            data = compute_tree(self.query_proxy, hospital, disease)
            resdata = {}
            for value in data.itervalues():
                res_data = hierarchy_flat(value)
                for k, v in res_data.iteritems():
                    resdata[k] = v
            return resdata

    def get_specific_by_path(self, rid, path, hospital='standard', disease='model'):
        self.logger.info("get_specific_disease_model rid: %s,path: %s,hospital: %s,disease: %s", rid, path, hospital,
                         disease)
        pathAttr = path.split('|')
        desc, mid = self.query_proxy.query_for_desc_by_key(None, path, hospital, disease)

        if desc is None:
            raise falcon.HTTPNotFound('not valid datapoint')
        else:
            resdata = {}
            resdata['desc'] = desc
            resdata['mid'] = mid
            return resdata


def hierarchy_flat(data):
    stack = Stack()
    res = {}
    node = {}
    node['options'] = data.options
    node['desc'] = data.alias
    node['multi'] = data.is_repeatable
    node['tpl'] = data.tpl
    res[data.path] = node
    stack.push(data)

    while (False == stack.isEmpty()):
        parent_node = stack.pop();

        for child in parent_node.children_node:
            tmp = {}
            tmp['options'] = child.options
            tmp['desc'] = child.alias
            tmp['multi'] = child.is_repeatable
            tmp['tpl'] = child.tpl
            res[child.path] = tmp
            stack.push(child)

    return res


def compute_relation(proxy, relationData, hospital, disease):
    stack = Stack()
    root_node = model2relation(proxy, relationData.widget_id)
    root_node.level = relationData.level
    stack.push(root_node)

    while (False == stack.isEmpty()):
        node = stack.pop()
        node.children_node = []
        children = proxy.query_for_relation_parent_detail(hospital, disease, node.widget_id).all()

        for child in children:
            child_node = model2relation(proxy, child.widget_id)
            child_node.level = child.level
            child_node.path = node.path + '|' + child_node.path
            stack.push(child_node)
            node.children_node.append(child_node)

    return root_node


def compute_tree(proxy, hospital, disease):
    data = proxy.query_for_relation_all(hospital, disease, 1)

    dictMerged = {}
    for item in data:
        root_node = compute_relation(proxy, item, hospital, disease)
        dictMerged[root_node.path] = root_node
    return dictMerged


def model2relation(proxy, widget_id):
    root_node = RelationNode()
    widget = proxy.query_for_widget_detail(widget_id)
    root_node.tpl = widget.tpl
    root_node.alias = widget.alias
    root_node.widget_id = widget.widget_id
    root_node.is_repeatable = widget.is_repeatable
    root_node.key_id = widget.key_id
    root_node.path = widget.path
    return root_node

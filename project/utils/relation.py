# –*- encoding:utf8 –*-

__author__ = 'jiyue'


class RelationNode(object):
    tpl = ''
    alias = ''
    path = ''
    is_repeatable = ''
    options = ''
    key_id = 0
    is_leaf = 0
    level = 0
    widget_id = 0

    def __str__(self):
        return super(RelationNode, self).__str__()

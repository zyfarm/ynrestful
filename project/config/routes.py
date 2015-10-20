from project.biz.biz_controller import MetaPointsController, DataModelController, WidgetController

__author__ = 'jiyue'

registed_services = {
    'meta_points': MetaPointsController(),
    'data_models': DataModelController(),
    'widgets': WidgetController()
}

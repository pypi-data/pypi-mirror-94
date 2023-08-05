from aishu import setting
def sql(key):
    """
    对应数据服务的sql语句注册
    :param key:
    :return:
    """
    switcher = {
        'UserID':{'sql':'select userId from User where loginName = "admin";','database':'AnyRobot'},
        'MLID': {'sql': "select id from MLJob ;", 'database': 'AnyRobotML'},
        'entityID': {'sql': "select id from Entity;", 'database': 'AnyRobot'},
        'groupID': {'sql': "select id from EntityGroup;", 'database': 'AnyRobot'},
        'AlertRuleID': {'sql': "select id from RuleEngineAlert;", 'database': 'AnyRobot'},
        'kpiID': {'sql': "select id from DBIOKpi;", 'database': 'AnyRobot'},
        'AddEntityID': {'sql': "select entityId from ConditionKey where conditionValues = '192.168.84.26' AND conditionKeys = 'host';",'database': 'AnyRobot'}
    }

    if switcher.get(key) is not None:
        if switcher[key].get('database') is not None:
            if len(switcher[key]['database']) == 0:
                setting.database = 'AnyRobot'
            else:
                setting.database = switcher[key]['database']

        return switcher[key]['sql']
    else:
        return False

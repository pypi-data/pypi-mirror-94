#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2019 NetEase.com, Inc. All Rights Reserved.
# Copyright 2019, The nsh-item Recommendation Project, The User Persona Group, The Fuxi AI Lab.
"""
exec_hive

Authors: wangkai02(wangkai02@corp.netease.com)
Phone: 17816029211
Date: 2019/2/18
"""

from .impala_utils import ImpalaUtils


def exec_hive(sqlfiles, ds, conn_type='impala'):
    """ Processing data through Hive platform and Impala platform.

    Args:
        sqlfiles (List): list of sql files
        ds (str): run sql in 'ds' day
        conn_type (str): 'hive' or 'impala'

    Returns:

    """
    impala_handler = ImpalaUtils('impala')
    hive_handler = ImpalaUtils('hive')
    for sqlfile in sqlfiles:
        USER_QUERY_SQL = open(sqlfile, 'r', encoding='utf8').read()
        USER_QUERY_SQLs = list(filter(None, USER_QUERY_SQL.split(';;')))
        for i in range(len(USER_QUERY_SQLs)):
            user_sql = USER_QUERY_SQLs[i].replace('2019-04-01', ds)
            print('exec_sql: ', user_sql)
            if (conn_type=='impala' and '--hive' not in user_sql.lower()) or 'invalidate' in user_sql.lower():
                df = impala_handler.exec_sql_dml(sql=user_sql)
            else:
                df = hive_handler.exec_sql_dml(sql=user_sql)
    impala_handler.close_conn()
    hive_handler.close_conn()

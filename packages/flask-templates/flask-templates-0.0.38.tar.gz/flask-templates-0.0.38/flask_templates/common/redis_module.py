# -*- coding: utf-8 -*-
"""
----------------------------------------------------
    File Name:              redis_module
    Description             
    Author:                 develop
    date:                   2019/4/8
----------------------------------------------------
"""
__author__ = 'develop'

from hashlib import md5
from threading import Lock
from redis import Redis, ConnectionPool, sentinel
from copy import deepcopy
from flask_templates.common.utils import decrypt
from flask_templates.configs.template import REDIS_CONFIG

_MANAGER_LOCKS = Lock()


class MyRedis(object):
    """Redis连接类"""

    INSTANCE = {}

    def __new__(cls, redis_name=None):
        """
        singleton redis constructor
        :param redis_name: redis_name string in application.yaml
        :return:
        """
        e_type = 'special' if REDIS_CONFIG.get('encryption') else None
        if not redis_name:
            redis_config = deepcopy(REDIS_CONFIG.get('default'))
        else:
            redis_config = deepcopy(REDIS_CONFIG.get(redis_name))
            if not redis_config:
                raise Exception("no such redis configs named `{}`".format(redis_name))
        config_hash = md5("".join(map(
            lambda i: "{}{}".format(i[0], i[1]), sorted(redis_config.items())
        )).encode()).hexdigest()
        if config_hash in cls.INSTANCE:
            return cls.INSTANCE[config_hash]
        with _MANAGER_LOCKS:
            if config_hash not in cls.INSTANCE:
                instance = object.__new__(cls)
                redis_config['host'] = [x.strip() for x in redis_config['host'].split(',')]
                redis_config['port'] = [int(x.strip()) for x in str(redis_config['port']).split(',')]
                redis_config['password'] = decrypt(redis_config['password'], e_type)
                use_sentinel = redis_config.pop('use_sentinel') if 'use_sentinel' in redis_config else False
                if use_sentinel:
                    st = sentinel.Sentinel(list(zip(redis_config.pop('host'), redis_config.pop('port'))))
                    instance.master = st.master_for(redis_name, **redis_config)
                    instance.slave = st.slave_for(redis_name, **redis_config)
                else:
                    redis_config['host'] = redis_config['host'][0]
                    redis_config['port'] = redis_config['port'][0]
                    pool = ConnectionPool(**redis_config)  # decode_responses=True保证解析出来的不是bytes类型
                    instance.master = instance.slave = Redis(connection_pool=pool)
                cls.INSTANCE[config_hash] = instance
        return cls.INSTANCE[config_hash]

    def get_redis_client(self, master=True):
        """返回一个Redis对象的实例"""
        if master:
            return self.master
        return self.slave


if __name__ == '__main__':
    myredis = MyRedis('default')
    print(myredis.get_redis_client())

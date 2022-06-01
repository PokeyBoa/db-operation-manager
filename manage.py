# -*- coding: UTF-8 -*-
__author__ = 'Pokeyboa'
__date__ = '2022.05.27'

"""
[ A Test Case ]
Redis database operations, more advanced code module encapsulation.

First, dynamically configure in Yaml file:
1. Establish a connection to the database
2. Terminal printing of logs

So you just need to focus on the business logic itself.
"""

import sys

from config.settings import BASE_PATH
sys.path.append(BASE_PATH)

from service.example import redis_curd_demo as main


if __name__ == '__main__':
    main()


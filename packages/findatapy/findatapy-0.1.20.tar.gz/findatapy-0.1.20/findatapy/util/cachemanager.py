__author__ = 'saeedamen' # Saeed Amen

#
# Copyright 2016 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#

from findatapy.util.singleton import Singleton

class CacheManager(object):
    __metaclass__ = Singleton

    _is_init = 0

    _dict_cache = {}

    def __init__(self, *args, **kwargs):
        if CacheManager._is_init == 0:
            # CacheManager.populate_time_series_dictionaries()
            CacheManager._is_init = 1
        pass

    ### time series ticker manipulators
    @staticmethod
    def add_cache(key, obj):
        CacheManager._dict_cache[key] = obj

    @staticmethod
    def get_cache(key):
        if key in CacheManager._dict_cache:
            # print('cached ' + key)
            return CacheManager._dict_cache[key]

        return None

    @staticmethod
    def is_in_cache(key):
        return key in CacheManager._dict_cache

    @staticmethod
    def flush_cache():
        CacheManager._dict_cache = {}
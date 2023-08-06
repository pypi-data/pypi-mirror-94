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

import logging
import logging.config

from findatapy.util.dataconstants import DataConstants
from findatapy.util.singleton import Singleton

class LoggerManager(object):
    """Acts as a wrapper for logging.

    """
    __metaclass__ = Singleton

    _loggers = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def getLogger(name=None):
        if not name:
            try:
                logging.config.fileConfig(DataConstants().logging_conf)
            except: pass

            log = logging.getLogger();
        elif name not in LoggerManager._loggers.keys():
            try:
                logging.config.fileConfig(DataConstants().logging_conf)
            except: pass

            LoggerManager._loggers[name] = logging.getLogger(str(name))

        log = LoggerManager._loggers[name]

        # when recalling appears to make other loggers disabled
        # hence apply this hack!
        for name in LoggerManager._loggers.keys():
            LoggerManager._loggers[name].disabled = False

        return log

if __name__ == '__main__':

    logger = LoggerManager.getLogger(__name__)

    logger.info("Hello")
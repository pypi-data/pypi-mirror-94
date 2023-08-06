# -*- coding: utf-8 -*-
""" Copyright 2020 Marco Arrigoni

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging
import sys

verbose_log = True

if verbose_log:
    LOGGING_CONF_FORMAT = ('%(created)f - %(asctime)s - %(name)s '
                          '- %(levelname)s - %(message)s '
                          '- on line: %(lineno)d in file: %(filename)s')
else:
    LOGGING_CONF_FORMAT = ('%(created)f - %(asctime)s '
                          '- %(levelname)s - %(message)s')

LOGGING_DATE_FORMAT = '%d.%m.%Y %I:%M:%S %p'
ROOT_LOGGER = logging.getLogger(__name__)
ROOT_LOGGER.setLevel(logging.DEBUG)

LOGFILE_NAME = '.evpdlogfile.log'
ROOT_FILE_HANDLER = logging.FileHandler(LOGFILE_NAME, mode='w')
ROOT_FORMATTER = logging.Formatter(LOGGING_CONF_FORMAT, 
                                   LOGGING_DATE_FORMAT)
ROOT_FILE_HANDLER.setFormatter(ROOT_FORMATTER)

ROOT_LOGGER.addHandler(ROOT_FILE_HANDLER)

caller = sys.argv[0]
SESSION_LOGGER = logging.getLogger(caller)
SESSION_LOGGER.setLevel(logging.DEBUG)
#SESSION_FILE_HANDLER = logging.FileHandler('logfile_' + caller.split('.')[0] + '.log')
#SESSION_FILE_HANDLER.setFormatter(ROOT_FORMATTER)
#SESSION_LOGGER.addHandler(SESSION_FILE_HANDLER)

# -*- coding: utf-8 -*-

import os
from robot.libraries.BuiltIn import BuiltIn
from robot.api import logger
from .keywordgroup import KeywordGroup


class _LoggingKeywords(KeywordGroup):

    # Private
    def _get_appium_log_level(self):
        return BuiltIn().get_variable_value("${APPIUM_LOG_LEVEL}", default='WARN')

    def _debug(self, message):
        apm_ll = self._get_appium_log_level()
        if apm_ll == 'DEBUG':
            logger.debug(message)

    def _get_log_dir(self):
        variables = BuiltIn().get_variables()
        logfile = variables['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return variables['${OUTPUTDIR}']

    def _html(self, message):
        logger.info(message, True, False)

    def _info(self, message):
        apm_ll = self._get_appium_log_level()
        if apm_ll == 'INFO' or apm_ll == 'DEBUG':
            logger.info(message)

    def _log(self, message, level='INFO'):
        level = level.upper()
        if (level == 'INFO'):
            self._info(message)
        elif (level == 'DEBUG'):
            self._debug(message)
        elif (level == 'WARN'):
            self._warn(message)
        elif (level == 'HTML'):
            self._html(message)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s', ''][len(items) == 1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items

    def _warn(self, message):
        apm_ll = self._get_appium_log_level()
        if apm_ll == 'WARN' or apm_ll == 'INFO' or apm_ll == 'DEBUG':
            logger.warn(message)

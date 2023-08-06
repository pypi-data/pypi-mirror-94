# -*- coding: utf-8 -*-
import json
import os

from omc.common import CmdTaskMixin
from omc.config import settings
from omc.core import Resource
from omc.core.decorator import filecache

from omc_jmx import utils


class Jmx(Resource, CmdTaskMixin):
    """
NAME
    jmx - jmx command

SYNOPSIS
    jmx [RESOURCE] action [OPTION]

ACTION LIST

    """

    def _description(self):
        return 'JMX(Java Management Extensions) Tool Set'

    def jvms(self):
        cmd = utils.JmxTermUtils.build_command('jvms')
        self.run_cmd(cmd)

    @filecache(duration=60 * 60 * 24, file=Resource._get_cache_file_name)
    def _completion(self, short_mode=True):
        results = []
        results.append(super()._completion(False))

        if not self._have_resource_value():
            # list rabbitmq connection instance from config file
            config_file_name = os.path.join(settings.CONFIG_DIR, self.__class__.__name__.lower() + '.json')
            if (os.path.exists(config_file_name)):
                with open(config_file_name) as f:
                    instances = json.load(f)
                    results.extend(
                        self._get_completion(
                            [(value.get('host') + ':' + str(value.get('port')), key) for key, value in
                             instances.items()],
                            False))

        return "\n".join(results)

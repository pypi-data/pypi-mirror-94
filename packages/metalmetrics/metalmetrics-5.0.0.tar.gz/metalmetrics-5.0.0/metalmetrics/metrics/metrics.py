# -*- coding: utf-8 -*-

from metalmetrics.config.config import ConfigFile
from metalmetrics.metrics.bare import Bare
from metalmetrics.printer.printer import Printer


class MetricsException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Metrics(object):
    def __init__(self, config):
        if config is None:
            raise MetricsException("config invalid")
        self._config = config
        self._spec = config.config_file.get(ConfigFile.SPEC, None)
        if self._spec is None:
            raise MetricsException("spec invalid")

    def _dump(self, data):
        printer = Printer()
        printer.run(data=data, name=self._config.output_file, append=False)

    def _instance(self):
        buf = {}
        buf[Bare.__name__.lower()] = Bare(self._config)
        return buf

    def routine(self, spec=None):
        specs = []
        if spec is None or len(spec) == 0:
            specs.extend(self._spec)
        else:
            specs.append(spec)
        buf = {}
        for key, val in self._instance().items():
            b = {}
            for item in specs:
                b[item] = val.run(item)
            buf[key] = b
        if len(self._config.output_file) != 0:
            self._dump(buf)
        return buf

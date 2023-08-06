# -*- coding: utf-8 -*-
"""
    test.rest.DummyCommandableHttpService
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Dummy commandable HTTP service
    
    :copyright: Conceptual Vision Consulting LLC 2015-2016, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from abc import ABC
from pip_services3_commons.refer import Descriptor
from pip_services3_rpc.services import CommandableHttpService

class DummyCommandableHttpService(CommandableHttpService, ABC):
    
    def __init__(self):
        super(DummyCommandableHttpService, self).__init__('dummy')
        self._dependency_resolver.put('controller', Descriptor('pip-services-dummies', 'controller', '*', '*', '*'))

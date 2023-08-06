'''_1908.py

OptimizationStrategy
'''


from typing import Generic, TypeVar

from mastapy.system_model.optimization import _1909, _1907
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_STRATEGY = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'OptimizationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationStrategy',)


TStep = TypeVar('TStep', bound='_1907.OptimizationStep')


class OptimizationStrategy(_1909.OptimizationStrategyBase, Generic[TStep]):
    '''OptimizationStrategy

    This is a mastapy class.

    Generic Types:
        TStep
    '''

    TYPE = _OPTIMIZATION_STRATEGY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationStrategy.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

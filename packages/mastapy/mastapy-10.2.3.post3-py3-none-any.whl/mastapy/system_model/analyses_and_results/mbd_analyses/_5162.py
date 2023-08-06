'''_5162.py

UnbalancedMassMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2077
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6277
from mastapy.system_model.analyses_and_results.mbd_analyses import _5163
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'UnbalancedMassMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassMultiBodyDynamicsAnalysis',)


class UnbalancedMassMultiBodyDynamicsAnalysis(_5163.VirtualComponentMultiBodyDynamicsAnalysis):
    '''UnbalancedMassMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2077.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2077.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6277.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6277.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[UnbalancedMassMultiBodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultiBodyDynamicsAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(UnbalancedMassMultiBodyDynamicsAnalysis))
        return value

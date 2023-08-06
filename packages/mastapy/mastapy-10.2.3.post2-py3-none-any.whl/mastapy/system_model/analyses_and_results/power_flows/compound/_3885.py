'''_3885.py

RingPinsCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows import _3755
from mastapy.system_model.analyses_and_results.power_flows.compound import _3873
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'RingPinsCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundPowerFlow',)


class RingPinsCompoundPowerFlow(_3873.MountableComponentCompoundPowerFlow):
    '''RingPinsCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2216.RingPins':
        '''RingPins: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2216.RingPins)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3755.RingPinsPowerFlow]':
        '''List[RingPinsPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3755.RingPinsPowerFlow))
        return value

    @property
    def component_power_flow_load_cases(self) -> 'List[_3755.RingPinsPowerFlow]':
        '''List[RingPinsPowerFlow]: 'ComponentPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentPowerFlowLoadCases, constructor.new(_3755.RingPinsPowerFlow))
        return value

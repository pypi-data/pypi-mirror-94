'''_2574.py

RingPinsCompoundSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.system_deflections import _2427
from mastapy.system_model.analyses_and_results.system_deflections.compound import _2562
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Compound', 'RingPinsCompoundSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundSystemDeflection',)


class RingPinsCompoundSystemDeflection(_2562.MountableComponentCompoundSystemDeflection):
    '''RingPinsCompoundSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_2427.RingPinsSystemDeflection]':
        '''List[RingPinsSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2427.RingPinsSystemDeflection))
        return value

    @property
    def component_system_deflection_load_cases(self) -> 'List[_2427.RingPinsSystemDeflection]':
        '''List[RingPinsSystemDeflection]: 'ComponentSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionLoadCases, constructor.new(_2427.RingPinsSystemDeflection))
        return value

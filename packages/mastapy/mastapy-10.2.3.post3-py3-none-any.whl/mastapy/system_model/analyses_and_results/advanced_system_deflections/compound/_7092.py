'''_7092.py

RingPinsCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.cycloidal import _2216
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6962
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import _7080
from mastapy._internal.python_net import python_net_import

_RING_PINS_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'RingPinsCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsCompoundAdvancedSystemDeflection',)


class RingPinsCompoundAdvancedSystemDeflection(_7080.MountableComponentCompoundAdvancedSystemDeflection):
    '''RingPinsCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsCompoundAdvancedSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6962.RingPinsAdvancedSystemDeflection]':
        '''List[RingPinsAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6962.RingPinsAdvancedSystemDeflection))
        return value

    @property
    def component_advanced_system_deflection_load_cases(self) -> 'List[_6962.RingPinsAdvancedSystemDeflection]':
        '''List[RingPinsAdvancedSystemDeflection]: 'ComponentAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentAdvancedSystemDeflectionLoadCases, constructor.new(_6962.RingPinsAdvancedSystemDeflection))
        return value

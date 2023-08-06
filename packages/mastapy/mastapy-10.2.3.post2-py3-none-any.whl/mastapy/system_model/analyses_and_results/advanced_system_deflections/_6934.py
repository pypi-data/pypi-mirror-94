'''_6934.py

HypoidGearAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2180
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6502
from mastapy.gears.rating.hypoid import _399
from mastapy.system_model.analyses_and_results.system_deflections import _2398
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6874
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'HypoidGearAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearAdvancedSystemDeflection',)


class HypoidGearAdvancedSystemDeflection(_6874.AGMAGleasonConicalGearAdvancedSystemDeflection):
    '''HypoidGearAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2180.HypoidGear':
        '''HypoidGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.HypoidGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6502.HypoidGearLoadCase':
        '''HypoidGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6502.HypoidGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_399.HypoidGearRating':
        '''HypoidGearRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_399.HypoidGearRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def component_system_deflection_results(self) -> 'List[_2398.HypoidGearSystemDeflection]':
        '''List[HypoidGearSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2398.HypoidGearSystemDeflection))
        return value

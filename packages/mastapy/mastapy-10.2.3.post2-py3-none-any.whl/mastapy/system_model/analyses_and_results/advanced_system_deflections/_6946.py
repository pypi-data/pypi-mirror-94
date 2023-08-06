'''_6946.py

KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2187
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6516
from mastapy.gears.rating.klingelnberg_spiral_bevel import _367
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6944, _6945, _6940
from mastapy.system_model.analyses_and_results.system_deflections import _2408
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection',)


class KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection(_6940.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2187.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6516.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6516.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_367.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_367.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_367.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_367.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_advanced_system_deflection(self) -> 'List[_6944.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsAdvancedSystemDeflection, constructor.new(_6944.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_advanced_system_deflection(self) -> 'List[_6945.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesAdvancedSystemDeflection, constructor.new(_6945.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2408.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2408.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection))
        return value

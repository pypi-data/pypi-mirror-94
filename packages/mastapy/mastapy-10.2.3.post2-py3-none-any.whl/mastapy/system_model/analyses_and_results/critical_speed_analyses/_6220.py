'''_6220.py

KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2187
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6516
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6218, _6219, _6214
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis(_6214.KlingelnbergCycloPalloidConicalGearSetCriticalSpeedAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCriticalSpeedAnalysis.TYPE'):
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
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_critical_speed_analysis(self) -> 'List[_6218.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCriticalSpeedAnalysis, constructor.new(_6218.KlingelnbergCycloPalloidSpiralBevelGearCriticalSpeedAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_critical_speed_analysis(self) -> 'List[_6219.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCriticalSpeedAnalysis, constructor.new(_6219.KlingelnbergCycloPalloidSpiralBevelGearMeshCriticalSpeedAnalysis))
        return value

'''_6376.py

SpiralBevelGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2190
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6374, _6375, _6293
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6247
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'SpiralBevelGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundCriticalSpeedAnalysis',)


class SpiralBevelGearSetCompoundCriticalSpeedAnalysis(_6293.BevelGearSetCompoundCriticalSpeedAnalysis):
    '''SpiralBevelGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2190.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2190.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2190.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_critical_speed_analysis(self) -> 'List[_6374.SpiralBevelGearCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearCompoundCriticalSpeedAnalysis]: 'SpiralBevelGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundCriticalSpeedAnalysis, constructor.new(_6374.SpiralBevelGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_critical_speed_analysis(self) -> 'List[_6375.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearMeshCompoundCriticalSpeedAnalysis]: 'SpiralBevelMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6375.SpiralBevelGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6247.SpiralBevelGearSetCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6247.SpiralBevelGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6247.SpiralBevelGearSetCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearSetCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6247.SpiralBevelGearSetCriticalSpeedAnalysis))
        return value

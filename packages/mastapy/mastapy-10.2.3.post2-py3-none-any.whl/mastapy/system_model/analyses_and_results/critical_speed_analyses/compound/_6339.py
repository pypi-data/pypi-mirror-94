'''_6339.py

HypoidGearSetCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2181
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6337, _6338, _6281
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6210
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'HypoidGearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundCriticalSpeedAnalysis',)


class HypoidGearSetCompoundCriticalSpeedAnalysis(_6281.AGMAGleasonConicalGearSetCompoundCriticalSpeedAnalysis):
    '''HypoidGearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2181.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_critical_speed_analysis(self) -> 'List[_6337.HypoidGearCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearCompoundCriticalSpeedAnalysis]: 'HypoidGearsCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundCriticalSpeedAnalysis, constructor.new(_6337.HypoidGearCompoundCriticalSpeedAnalysis))
        return value

    @property
    def hypoid_meshes_compound_critical_speed_analysis(self) -> 'List[_6338.HypoidGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[HypoidGearMeshCompoundCriticalSpeedAnalysis]: 'HypoidMeshesCompoundCriticalSpeedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundCriticalSpeedAnalysis, constructor.new(_6338.HypoidGearMeshCompoundCriticalSpeedAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_6210.HypoidGearSetCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6210.HypoidGearSetCriticalSpeedAnalysis))
        return value

    @property
    def assembly_critical_speed_analysis_load_cases(self) -> 'List[_6210.HypoidGearSetCriticalSpeedAnalysis]':
        '''List[HypoidGearSetCriticalSpeedAnalysis]: 'AssemblyCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyCriticalSpeedAnalysisLoadCases, constructor.new(_6210.HypoidGearSetCriticalSpeedAnalysis))
        return value

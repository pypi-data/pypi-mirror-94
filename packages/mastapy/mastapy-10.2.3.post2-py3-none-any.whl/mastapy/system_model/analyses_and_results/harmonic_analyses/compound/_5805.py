'''_5805.py

HypoidGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2181
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5803, _5804, _5747
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5645
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'HypoidGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundHarmonicAnalysis',)


class HypoidGearSetCompoundHarmonicAnalysis(_5747.AGMAGleasonConicalGearSetCompoundHarmonicAnalysis):
    '''HypoidGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundHarmonicAnalysis.TYPE'):
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
    def hypoid_gears_compound_harmonic_analysis(self) -> 'List[_5803.HypoidGearCompoundHarmonicAnalysis]':
        '''List[HypoidGearCompoundHarmonicAnalysis]: 'HypoidGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundHarmonicAnalysis, constructor.new(_5803.HypoidGearCompoundHarmonicAnalysis))
        return value

    @property
    def hypoid_meshes_compound_harmonic_analysis(self) -> 'List[_5804.HypoidGearMeshCompoundHarmonicAnalysis]':
        '''List[HypoidGearMeshCompoundHarmonicAnalysis]: 'HypoidMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundHarmonicAnalysis, constructor.new(_5804.HypoidGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5645.HypoidGearSetHarmonicAnalysis]':
        '''List[HypoidGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5645.HypoidGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5645.HypoidGearSetHarmonicAnalysis]':
        '''List[HypoidGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5645.HypoidGearSetHarmonicAnalysis))
        return value

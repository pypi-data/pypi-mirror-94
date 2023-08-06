'''_5851.py

StraightBevelGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2194
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5849, _5850, _5759
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5694
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'StraightBevelGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundHarmonicAnalysis',)


class StraightBevelGearSetCompoundHarmonicAnalysis(_5759.BevelGearSetCompoundHarmonicAnalysis):
    '''StraightBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2194.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2194.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_harmonic_analysis(self) -> 'List[_5849.StraightBevelGearCompoundHarmonicAnalysis]':
        '''List[StraightBevelGearCompoundHarmonicAnalysis]: 'StraightBevelGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundHarmonicAnalysis, constructor.new(_5849.StraightBevelGearCompoundHarmonicAnalysis))
        return value

    @property
    def straight_bevel_meshes_compound_harmonic_analysis(self) -> 'List[_5850.StraightBevelGearMeshCompoundHarmonicAnalysis]':
        '''List[StraightBevelGearMeshCompoundHarmonicAnalysis]: 'StraightBevelMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundHarmonicAnalysis, constructor.new(_5850.StraightBevelGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5694.StraightBevelGearSetHarmonicAnalysis]':
        '''List[StraightBevelGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5694.StraightBevelGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5694.StraightBevelGearSetHarmonicAnalysis]':
        '''List[StraightBevelGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5694.StraightBevelGearSetHarmonicAnalysis))
        return value

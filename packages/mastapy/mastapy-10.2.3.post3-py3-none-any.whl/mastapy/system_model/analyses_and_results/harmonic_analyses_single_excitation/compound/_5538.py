'''_5538.py

StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation
'''


from typing import List

from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import _5536, _5537, _5449
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5409
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound', 'StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation',)


class StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation(_5449.BevelGearSetCompoundHarmonicAnalysisOfSingleExcitation):
    '''StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2192.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.StraightBevelDiffGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2192.StraightBevelDiffGearSet':
        '''StraightBevelDiffGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2192.StraightBevelDiffGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_diff_gears_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5536.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffGearsCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5536.StraightBevelDiffGearCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def straight_bevel_diff_meshes_compound_harmonic_analysis_of_single_excitation(self) -> 'List[_5537.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation]: 'StraightBevelDiffMeshesCompoundHarmonicAnalysisOfSingleExcitation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundHarmonicAnalysisOfSingleExcitation, constructor.new(_5537.StraightBevelDiffGearMeshCompoundHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5409.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5409.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation))
        return value

    @property
    def assembly_harmonic_analysis_of_single_excitation_load_cases(self) -> 'List[_5409.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]':
        '''List[StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation]: 'AssemblyHarmonicAnalysisOfSingleExcitationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisOfSingleExcitationLoadCases, constructor.new(_5409.StraightBevelDiffGearSetHarmonicAnalysisOfSingleExcitation))
        return value

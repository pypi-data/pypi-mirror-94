'''_3635.py

StraightBevelDiffGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3633, _3634, _3546
from mastapy.system_model.analyses_and_results.stability_analyses import _3505
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'StraightBevelDiffGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundStabilityAnalysis',)


class StraightBevelDiffGearSetCompoundStabilityAnalysis(_3546.BevelGearSetCompoundStabilityAnalysis):
    '''StraightBevelDiffGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundStabilityAnalysis.TYPE'):
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
    def straight_bevel_diff_gears_compound_stability_analysis(self) -> 'List[_3633.StraightBevelDiffGearCompoundStabilityAnalysis]':
        '''List[StraightBevelDiffGearCompoundStabilityAnalysis]: 'StraightBevelDiffGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundStabilityAnalysis, constructor.new(_3633.StraightBevelDiffGearCompoundStabilityAnalysis))
        return value

    @property
    def straight_bevel_diff_meshes_compound_stability_analysis(self) -> 'List[_3634.StraightBevelDiffGearMeshCompoundStabilityAnalysis]':
        '''List[StraightBevelDiffGearMeshCompoundStabilityAnalysis]: 'StraightBevelDiffMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundStabilityAnalysis, constructor.new(_3634.StraightBevelDiffGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3505.StraightBevelDiffGearSetStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3505.StraightBevelDiffGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3505.StraightBevelDiffGearSetStabilityAnalysis]':
        '''List[StraightBevelDiffGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3505.StraightBevelDiffGearSetStabilityAnalysis))
        return value

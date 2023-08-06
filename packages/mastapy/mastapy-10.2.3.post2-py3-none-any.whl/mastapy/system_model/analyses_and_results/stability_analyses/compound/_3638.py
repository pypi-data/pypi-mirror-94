'''_3638.py

StraightBevelGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2194
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3636, _3637, _3546
from mastapy.system_model.analyses_and_results.stability_analyses import _3508
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'StraightBevelGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundStabilityAnalysis',)


class StraightBevelGearSetCompoundStabilityAnalysis(_3546.BevelGearSetCompoundStabilityAnalysis):
    '''StraightBevelGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundStabilityAnalysis.TYPE'):
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
    def straight_bevel_gears_compound_stability_analysis(self) -> 'List[_3636.StraightBevelGearCompoundStabilityAnalysis]':
        '''List[StraightBevelGearCompoundStabilityAnalysis]: 'StraightBevelGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundStabilityAnalysis, constructor.new(_3636.StraightBevelGearCompoundStabilityAnalysis))
        return value

    @property
    def straight_bevel_meshes_compound_stability_analysis(self) -> 'List[_3637.StraightBevelGearMeshCompoundStabilityAnalysis]':
        '''List[StraightBevelGearMeshCompoundStabilityAnalysis]: 'StraightBevelMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundStabilityAnalysis, constructor.new(_3637.StraightBevelGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3508.StraightBevelGearSetStabilityAnalysis]':
        '''List[StraightBevelGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3508.StraightBevelGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3508.StraightBevelGearSetStabilityAnalysis]':
        '''List[StraightBevelGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3508.StraightBevelGearSetStabilityAnalysis))
        return value

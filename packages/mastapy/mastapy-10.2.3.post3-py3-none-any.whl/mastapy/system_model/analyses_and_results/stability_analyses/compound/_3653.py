'''_3653.py

WormGearSetCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2198
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3651, _3652, _3588
from mastapy.system_model.analyses_and_results.stability_analyses import _3523
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'WormGearSetCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundStabilityAnalysis',)


class WormGearSetCompoundStabilityAnalysis(_3588.GearSetCompoundStabilityAnalysis):
    '''WormGearSetCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2198.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2198.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2198.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_stability_analysis(self) -> 'List[_3651.WormGearCompoundStabilityAnalysis]':
        '''List[WormGearCompoundStabilityAnalysis]: 'WormGearsCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundStabilityAnalysis, constructor.new(_3651.WormGearCompoundStabilityAnalysis))
        return value

    @property
    def worm_meshes_compound_stability_analysis(self) -> 'List[_3652.WormGearMeshCompoundStabilityAnalysis]':
        '''List[WormGearMeshCompoundStabilityAnalysis]: 'WormMeshesCompoundStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundStabilityAnalysis, constructor.new(_3652.WormGearMeshCompoundStabilityAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3523.WormGearSetStabilityAnalysis]':
        '''List[WormGearSetStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3523.WormGearSetStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3523.WormGearSetStabilityAnalysis]':
        '''List[WormGearSetStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3523.WormGearSetStabilityAnalysis))
        return value

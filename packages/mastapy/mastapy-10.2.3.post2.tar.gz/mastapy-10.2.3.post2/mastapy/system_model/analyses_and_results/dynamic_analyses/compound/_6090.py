'''_6090.py

StraightBevelGearSetCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2146
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6088, _6089, _6004
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5969
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'StraightBevelGearSetCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetCompoundDynamicAnalysis',)


class StraightBevelGearSetCompoundDynamicAnalysis(_6004.BevelGearSetCompoundDynamicAnalysis):
    '''StraightBevelGearSetCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2146.StraightBevelGearSet':
        '''StraightBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2146.StraightBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2146.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2146.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def straight_bevel_gears_compound_dynamic_analysis(self) -> 'List[_6088.StraightBevelGearCompoundDynamicAnalysis]':
        '''List[StraightBevelGearCompoundDynamicAnalysis]: 'StraightBevelGearsCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsCompoundDynamicAnalysis, constructor.new(_6088.StraightBevelGearCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_meshes_compound_dynamic_analysis(self) -> 'List[_6089.StraightBevelGearMeshCompoundDynamicAnalysis]':
        '''List[StraightBevelGearMeshCompoundDynamicAnalysis]: 'StraightBevelMeshesCompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesCompoundDynamicAnalysis, constructor.new(_6089.StraightBevelGearMeshCompoundDynamicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5969.StraightBevelGearSetDynamicAnalysis]':
        '''List[StraightBevelGearSetDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5969.StraightBevelGearSetDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_5969.StraightBevelGearSetDynamicAnalysis]':
        '''List[StraightBevelGearSetDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_5969.StraightBevelGearSetDynamicAnalysis))
        return value

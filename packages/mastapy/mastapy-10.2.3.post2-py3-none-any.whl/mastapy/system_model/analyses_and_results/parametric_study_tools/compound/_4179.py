'''_4179.py

StraightBevelDiffGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2192
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4177, _4178, _4090
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4050
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'StraightBevelDiffGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelDiffGearSetCompoundParametricStudyTool',)


class StraightBevelDiffGearSetCompoundParametricStudyTool(_4090.BevelGearSetCompoundParametricStudyTool):
    '''StraightBevelDiffGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_DIFF_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelDiffGearSetCompoundParametricStudyTool.TYPE'):
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
    def straight_bevel_diff_gears_compound_parametric_study_tool(self) -> 'List[_4177.StraightBevelDiffGearCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearCompoundParametricStudyTool]: 'StraightBevelDiffGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearsCompoundParametricStudyTool, constructor.new(_4177.StraightBevelDiffGearCompoundParametricStudyTool))
        return value

    @property
    def straight_bevel_diff_meshes_compound_parametric_study_tool(self) -> 'List[_4178.StraightBevelDiffGearMeshCompoundParametricStudyTool]':
        '''List[StraightBevelDiffGearMeshCompoundParametricStudyTool]: 'StraightBevelDiffMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffMeshesCompoundParametricStudyTool, constructor.new(_4178.StraightBevelDiffGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4050.StraightBevelDiffGearSetParametricStudyTool]':
        '''List[StraightBevelDiffGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4050.StraightBevelDiffGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4050.StraightBevelDiffGearSetParametricStudyTool]':
        '''List[StraightBevelDiffGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4050.StraightBevelDiffGearSetParametricStudyTool))
        return value

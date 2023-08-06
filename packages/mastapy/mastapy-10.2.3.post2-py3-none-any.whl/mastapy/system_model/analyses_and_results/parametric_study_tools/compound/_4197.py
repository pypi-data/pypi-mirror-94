'''_4197.py

WormGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2198
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4195, _4196, _4132
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4068
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'WormGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundParametricStudyTool',)


class WormGearSetCompoundParametricStudyTool(_4132.GearSetCompoundParametricStudyTool):
    '''WormGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundParametricStudyTool.TYPE'):
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
    def worm_gears_compound_parametric_study_tool(self) -> 'List[_4195.WormGearCompoundParametricStudyTool]':
        '''List[WormGearCompoundParametricStudyTool]: 'WormGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundParametricStudyTool, constructor.new(_4195.WormGearCompoundParametricStudyTool))
        return value

    @property
    def worm_meshes_compound_parametric_study_tool(self) -> 'List[_4196.WormGearMeshCompoundParametricStudyTool]':
        '''List[WormGearMeshCompoundParametricStudyTool]: 'WormMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundParametricStudyTool, constructor.new(_4196.WormGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4068.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4068.WormGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4068.WormGearSetParametricStudyTool]':
        '''List[WormGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4068.WormGearSetParametricStudyTool))
        return value

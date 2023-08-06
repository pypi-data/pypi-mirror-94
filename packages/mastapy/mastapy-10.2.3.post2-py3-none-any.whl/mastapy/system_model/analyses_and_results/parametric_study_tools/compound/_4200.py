'''_4200.py

ZerolBevelGearSetCompoundParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.gears import _2200
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.parametric_study_tools.compound import _4198, _4199, _4090
from mastapy.system_model.analyses_and_results.parametric_study_tools import _4071
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.Compound', 'ZerolBevelGearSetCompoundParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundParametricStudyTool',)


class ZerolBevelGearSetCompoundParametricStudyTool(_4090.BevelGearSetCompoundParametricStudyTool):
    '''ZerolBevelGearSetCompoundParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2200.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2200.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_parametric_study_tool(self) -> 'List[_4198.ZerolBevelGearCompoundParametricStudyTool]':
        '''List[ZerolBevelGearCompoundParametricStudyTool]: 'ZerolBevelGearsCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundParametricStudyTool, constructor.new(_4198.ZerolBevelGearCompoundParametricStudyTool))
        return value

    @property
    def zerol_bevel_meshes_compound_parametric_study_tool(self) -> 'List[_4199.ZerolBevelGearMeshCompoundParametricStudyTool]':
        '''List[ZerolBevelGearMeshCompoundParametricStudyTool]: 'ZerolBevelMeshesCompoundParametricStudyTool' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundParametricStudyTool, constructor.new(_4199.ZerolBevelGearMeshCompoundParametricStudyTool))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4071.ZerolBevelGearSetParametricStudyTool]':
        '''List[ZerolBevelGearSetParametricStudyTool]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4071.ZerolBevelGearSetParametricStudyTool))
        return value

    @property
    def assembly_parametric_study_tool_load_cases(self) -> 'List[_4071.ZerolBevelGearSetParametricStudyTool]':
        '''List[ZerolBevelGearSetParametricStudyTool]: 'AssemblyParametricStudyToolLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyParametricStudyToolLoadCases, constructor.new(_4071.ZerolBevelGearSetParametricStudyTool))
        return value

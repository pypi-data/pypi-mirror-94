'''_4579.py

HypoidGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2133
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6205
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4578, _4577, _4526
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'HypoidGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetModalAnalysisAtASpeed',)


class HypoidGearSetModalAnalysisAtASpeed(_4526.AGMAGleasonConicalGearSetModalAnalysisAtASpeed):
    '''HypoidGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2133.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6205.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6205.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_modal_analysis_at_a_speed(self) -> 'List[_4578.HypoidGearModalAnalysisAtASpeed]':
        '''List[HypoidGearModalAnalysisAtASpeed]: 'HypoidGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsModalAnalysisAtASpeed, constructor.new(_4578.HypoidGearModalAnalysisAtASpeed))
        return value

    @property
    def hypoid_meshes_modal_analysis_at_a_speed(self) -> 'List[_4577.HypoidGearMeshModalAnalysisAtASpeed]':
        '''List[HypoidGearMeshModalAnalysisAtASpeed]: 'HypoidMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesModalAnalysisAtASpeed, constructor.new(_4577.HypoidGearMeshModalAnalysisAtASpeed))
        return value

'''_4737.py

SpiralBevelGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2142
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4735, _4736, _4660
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4616
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'SpiralBevelGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundModalAnalysisAtASpeed',)


class SpiralBevelGearSetCompoundModalAnalysisAtASpeed(_4660.BevelGearSetCompoundModalAnalysisAtASpeed):
    '''SpiralBevelGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2142.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4735.SpiralBevelGearCompoundModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearCompoundModalAnalysisAtASpeed]: 'SpiralBevelGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundModalAnalysisAtASpeed, constructor.new(_4735.SpiralBevelGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def spiral_bevel_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4736.SpiralBevelGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearMeshCompoundModalAnalysisAtASpeed]: 'SpiralBevelMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4736.SpiralBevelGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4616.SpiralBevelGearSetModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4616.SpiralBevelGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4616.SpiralBevelGearSetModalAnalysisAtASpeed]':
        '''List[SpiralBevelGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4616.SpiralBevelGearSetModalAnalysisAtASpeed))
        return value

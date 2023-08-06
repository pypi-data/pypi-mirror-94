'''_4533.py

BevelDifferentialGearSetModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6129
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4532, _4531, _4538
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'BevelDifferentialGearSetModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearSetModalAnalysisAtASpeed',)


class BevelDifferentialGearSetModalAnalysisAtASpeed(_4538.BevelGearSetModalAnalysisAtASpeed):
    '''BevelDifferentialGearSetModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_SET_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearSetModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2114.BevelDifferentialGearSet':
        '''BevelDifferentialGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.BevelDifferentialGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6129.BevelDifferentialGearSetLoadCase':
        '''BevelDifferentialGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6129.BevelDifferentialGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bevel_differential_gears_modal_analysis_at_a_speed(self) -> 'List[_4532.BevelDifferentialGearModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearModalAnalysisAtASpeed]: 'BevelDifferentialGearsModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearsModalAnalysisAtASpeed, constructor.new(_4532.BevelDifferentialGearModalAnalysisAtASpeed))
        return value

    @property
    def bevel_differential_meshes_modal_analysis_at_a_speed(self) -> 'List[_4531.BevelDifferentialGearMeshModalAnalysisAtASpeed]':
        '''List[BevelDifferentialGearMeshModalAnalysisAtASpeed]: 'BevelDifferentialMeshesModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialMeshesModalAnalysisAtASpeed, constructor.new(_4531.BevelDifferentialGearMeshModalAnalysisAtASpeed))
        return value

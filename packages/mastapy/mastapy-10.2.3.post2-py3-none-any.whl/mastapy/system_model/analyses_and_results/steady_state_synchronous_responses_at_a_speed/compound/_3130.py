'''_3130.py

WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2198
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import _3128, _3129, _3065
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _3000
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed',)


class WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed(_3065.GearSetCompoundSteadyStateSynchronousResponseAtASpeed):
    '''WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
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
    def worm_gears_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3128.WormGearCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearCompoundSteadyStateSynchronousResponseAtASpeed]: 'WormGearsCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3128.WormGearCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def worm_meshes_compound_steady_state_synchronous_response_at_a_speed(self) -> 'List[_3129.WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed]: 'WormMeshesCompoundSteadyStateSynchronousResponseAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundSteadyStateSynchronousResponseAtASpeed, constructor.new(_3129.WormGearMeshCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3000.WormGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSetSteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3000.WormGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_3000.WormGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSetSteadyStateSynchronousResponseAtASpeed]: 'AssemblySteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_3000.WormGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

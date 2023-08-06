'''_2994.py

TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2253
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6573
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2913
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_PUMP_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed',)


class TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed(_2913.CouplingHalfSteadyStateSynchronousResponseAtASpeed):
    '''TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_PUMP_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterPumpSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2253.TorqueConverterPump':
        '''TorqueConverterPump: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2253.TorqueConverterPump)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6573.TorqueConverterPumpLoadCase':
        '''TorqueConverterPumpLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6573.TorqueConverterPumpLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

'''_3227.py

RollingRingConnectionSteadyStateSynchronousResponse
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1945
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6542
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3200
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'RollingRingConnectionSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingConnectionSteadyStateSynchronousResponse',)


class RollingRingConnectionSteadyStateSynchronousResponse(_3200.InterMountableComponentConnectionSteadyStateSynchronousResponse):
    '''RollingRingConnectionSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_CONNECTION_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingConnectionSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1945.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1945.RollingRingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6542.RollingRingConnectionLoadCase':
        '''RollingRingConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6542.RollingRingConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def planetaries(self) -> 'List[RollingRingConnectionSteadyStateSynchronousResponse]':
        '''List[RollingRingConnectionSteadyStateSynchronousResponse]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingConnectionSteadyStateSynchronousResponse))
        return value

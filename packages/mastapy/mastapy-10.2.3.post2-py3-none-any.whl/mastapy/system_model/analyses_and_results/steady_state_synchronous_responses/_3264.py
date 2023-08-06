'''_3264.py

ZerolBevelGearMeshSteadyStateSynchronousResponse
'''


from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6585
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3150
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'ZerolBevelGearMeshSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshSteadyStateSynchronousResponse',)


class ZerolBevelGearMeshSteadyStateSynchronousResponse(_3150.BevelGearMeshSteadyStateSynchronousResponse):
    '''ZerolBevelGearMeshSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1985.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6585.ZerolBevelGearMeshLoadCase':
        '''ZerolBevelGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6585.ZerolBevelGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

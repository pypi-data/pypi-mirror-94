'''_6209.py

HypoidGearMeshCriticalSpeedAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1969
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6503
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6149
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'HypoidGearMeshCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshCriticalSpeedAnalysis',)


class HypoidGearMeshCriticalSpeedAnalysis(_6149.AGMAGleasonConicalGearMeshCriticalSpeedAnalysis):
    '''HypoidGearMeshCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1969.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1969.HypoidGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6503.HypoidGearMeshLoadCase':
        '''HypoidGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6503.HypoidGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

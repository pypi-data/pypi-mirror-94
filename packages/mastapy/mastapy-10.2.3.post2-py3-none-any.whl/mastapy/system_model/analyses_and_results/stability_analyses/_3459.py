'''_3459.py

HypoidGearMeshStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1969
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6503
from mastapy.system_model.analyses_and_results.stability_analyses import _3400
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_MESH_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'HypoidGearMeshStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearMeshStabilityAnalysis',)


class HypoidGearMeshStabilityAnalysis(_3400.AGMAGleasonConicalGearMeshStabilityAnalysis):
    '''HypoidGearMeshStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_MESH_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearMeshStabilityAnalysis.TYPE'):
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

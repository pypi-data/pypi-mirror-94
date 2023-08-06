'''_3522.py

WormGearMeshStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets.gears import _1983
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6582
from mastapy.system_model.analyses_and_results.stability_analyses import _3455
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'WormGearMeshStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshStabilityAnalysis',)


class WormGearMeshStabilityAnalysis(_3455.GearMeshStabilityAnalysis):
    '''WormGearMeshStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1983.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6582.WormGearMeshLoadCase':
        '''WormGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6582.WormGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

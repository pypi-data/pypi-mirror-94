'''_6733.py

WormGearMeshAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.connections_and_sockets.gears import _1983
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6582
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6667
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'WormGearMeshAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshAdvancedTimeSteppingAnalysisForModulation',)


class WormGearMeshAdvancedTimeSteppingAnalysisForModulation(_6667.GearMeshAdvancedTimeSteppingAnalysisForModulation):
    '''WormGearMeshAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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

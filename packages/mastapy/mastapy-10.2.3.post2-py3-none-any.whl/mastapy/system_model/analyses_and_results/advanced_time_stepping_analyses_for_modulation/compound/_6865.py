'''_6865.py

ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1985
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6736
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6755
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation',)


class ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation(_6755.BevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_MESH_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearMeshCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1985.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.ZerolBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1985.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1985.ZerolBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6736.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6736.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def connection_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6736.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]':
        '''List[ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation]: 'ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6736.ZerolBevelGearMeshAdvancedTimeSteppingAnalysisForModulation))
        return value

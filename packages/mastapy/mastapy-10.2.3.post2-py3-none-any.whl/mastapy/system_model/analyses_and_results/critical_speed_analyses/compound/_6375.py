'''_6375.py

SpiralBevelGearMeshCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1977
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6246
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6292
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'SpiralBevelGearMeshCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshCompoundCriticalSpeedAnalysis',)


class SpiralBevelGearMeshCompoundCriticalSpeedAnalysis(_6292.BevelGearMeshCompoundCriticalSpeedAnalysis):
    '''SpiralBevelGearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1977.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.SpiralBevelGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1977.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1977.SpiralBevelGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6246.SpiralBevelGearMeshCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearMeshCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6246.SpiralBevelGearMeshCriticalSpeedAnalysis))
        return value

    @property
    def connection_critical_speed_analysis_load_cases(self) -> 'List[_6246.SpiralBevelGearMeshCriticalSpeedAnalysis]':
        '''List[SpiralBevelGearMeshCriticalSpeedAnalysis]: 'ConnectionCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionCriticalSpeedAnalysisLoadCases, constructor.new(_6246.SpiralBevelGearMeshCriticalSpeedAnalysis))
        return value

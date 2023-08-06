'''_6323.py

CylindricalGearMeshCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1963
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6194
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6334
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'CylindricalGearMeshCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearMeshCompoundCriticalSpeedAnalysis',)


class CylindricalGearMeshCompoundCriticalSpeedAnalysis(_6334.GearMeshCompoundCriticalSpeedAnalysis):
    '''CylindricalGearMeshCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MESH_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearMeshCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1963.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.CylindricalGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1963.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1963.CylindricalGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6194.CylindricalGearMeshCriticalSpeedAnalysis]':
        '''List[CylindricalGearMeshCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6194.CylindricalGearMeshCriticalSpeedAnalysis))
        return value

    @property
    def connection_critical_speed_analysis_load_cases(self) -> 'List[_6194.CylindricalGearMeshCriticalSpeedAnalysis]':
        '''List[CylindricalGearMeshCriticalSpeedAnalysis]: 'ConnectionCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionCriticalSpeedAnalysisLoadCases, constructor.new(_6194.CylindricalGearMeshCriticalSpeedAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearMeshCompoundCriticalSpeedAnalysis]':
        '''List[CylindricalGearMeshCompoundCriticalSpeedAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearMeshCompoundCriticalSpeedAnalysis))
        return value

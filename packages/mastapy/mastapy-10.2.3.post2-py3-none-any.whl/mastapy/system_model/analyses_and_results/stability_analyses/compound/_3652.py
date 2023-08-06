'''_3652.py

WormGearMeshCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1983
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3522
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3587
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'WormGearMeshCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearMeshCompoundStabilityAnalysis',)


class WormGearMeshCompoundStabilityAnalysis(_3587.GearMeshCompoundStabilityAnalysis):
    '''WormGearMeshCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_MESH_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearMeshCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1983.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.WormGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1983.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1983.WormGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3522.WormGearMeshStabilityAnalysis]':
        '''List[WormGearMeshStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3522.WormGearMeshStabilityAnalysis))
        return value

    @property
    def connection_stability_analysis_load_cases(self) -> 'List[_3522.WormGearMeshStabilityAnalysis]':
        '''List[WormGearMeshStabilityAnalysis]: 'ConnectionStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionStabilityAnalysisLoadCases, constructor.new(_3522.WormGearMeshStabilityAnalysis))
        return value

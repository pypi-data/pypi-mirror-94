'''_5795.py

FaceGearMeshCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1965
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5627
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5800
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'FaceGearMeshCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshCompoundHarmonicAnalysis',)


class FaceGearMeshCompoundHarmonicAnalysis(_5800.GearMeshCompoundHarmonicAnalysis):
    '''FaceGearMeshCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1965.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.FaceGearMesh)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1965.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5627.FaceGearMeshHarmonicAnalysis]':
        '''List[FaceGearMeshHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5627.FaceGearMeshHarmonicAnalysis))
        return value

    @property
    def connection_harmonic_analysis_load_cases(self) -> 'List[_5627.FaceGearMeshHarmonicAnalysis]':
        '''List[FaceGearMeshHarmonicAnalysis]: 'ConnectionHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionHarmonicAnalysisLoadCases, constructor.new(_5627.FaceGearMeshHarmonicAnalysis))
        return value

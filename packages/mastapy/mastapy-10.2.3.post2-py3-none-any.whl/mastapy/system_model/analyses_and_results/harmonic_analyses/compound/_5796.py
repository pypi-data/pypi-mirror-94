'''_5796.py

FaceGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2175
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5794, _5795, _5801
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5628
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'FaceGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetCompoundHarmonicAnalysis',)


class FaceGearSetCompoundHarmonicAnalysis(_5801.GearSetCompoundHarmonicAnalysis):
    '''FaceGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2175.FaceGearSet':
        '''FaceGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.FaceGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2175.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def face_gears_compound_harmonic_analysis(self) -> 'List[_5794.FaceGearCompoundHarmonicAnalysis]':
        '''List[FaceGearCompoundHarmonicAnalysis]: 'FaceGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsCompoundHarmonicAnalysis, constructor.new(_5794.FaceGearCompoundHarmonicAnalysis))
        return value

    @property
    def face_meshes_compound_harmonic_analysis(self) -> 'List[_5795.FaceGearMeshCompoundHarmonicAnalysis]':
        '''List[FaceGearMeshCompoundHarmonicAnalysis]: 'FaceMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesCompoundHarmonicAnalysis, constructor.new(_5795.FaceGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5628.FaceGearSetHarmonicAnalysis]':
        '''List[FaceGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5628.FaceGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5628.FaceGearSetHarmonicAnalysis]':
        '''List[FaceGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5628.FaceGearSetHarmonicAnalysis))
        return value

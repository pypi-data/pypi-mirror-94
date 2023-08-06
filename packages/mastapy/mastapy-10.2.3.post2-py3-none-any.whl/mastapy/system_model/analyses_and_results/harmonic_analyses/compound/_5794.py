'''_5794.py

FaceGearCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2174
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5626
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5799
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'FaceGearCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearCompoundHarmonicAnalysis',)


class FaceGearCompoundHarmonicAnalysis(_5799.GearCompoundHarmonicAnalysis):
    '''FaceGearCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2174.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5626.FaceGearHarmonicAnalysis]':
        '''List[FaceGearHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5626.FaceGearHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5626.FaceGearHarmonicAnalysis]':
        '''List[FaceGearHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5626.FaceGearHarmonicAnalysis))
        return value

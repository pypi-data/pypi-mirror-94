'''_5792.py

DatumCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2097
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5613
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5766
from mastapy._internal.python_net import python_net_import

_DATUM_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'DatumCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumCompoundHarmonicAnalysis',)


class DatumCompoundHarmonicAnalysis(_5766.ComponentCompoundHarmonicAnalysis):
    '''DatumCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _DATUM_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2097.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2097.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5613.DatumHarmonicAnalysis]':
        '''List[DatumHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5613.DatumHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5613.DatumHarmonicAnalysis]':
        '''List[DatumHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5613.DatumHarmonicAnalysis))
        return value

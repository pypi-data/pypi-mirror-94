'''_5833.py

RollingRingCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2242
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5675
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5780
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'RollingRingCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingCompoundHarmonicAnalysis',)


class RollingRingCompoundHarmonicAnalysis(_5780.CouplingHalfCompoundHarmonicAnalysis):
    '''RollingRingCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2242.RollingRing':
        '''RollingRing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2242.RollingRing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5675.RollingRingHarmonicAnalysis]':
        '''List[RollingRingHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5675.RollingRingHarmonicAnalysis))
        return value

    @property
    def component_harmonic_analysis_load_cases(self) -> 'List[_5675.RollingRingHarmonicAnalysis]':
        '''List[RollingRingHarmonicAnalysis]: 'ComponentHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentHarmonicAnalysisLoadCases, constructor.new(_5675.RollingRingHarmonicAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[RollingRingCompoundHarmonicAnalysis]':
        '''List[RollingRingCompoundHarmonicAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(RollingRingCompoundHarmonicAnalysis))
        return value

'''_3557.py

ConceptGearCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2167
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3427
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3586
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'ConceptGearCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearCompoundStabilityAnalysis',)


class ConceptGearCompoundStabilityAnalysis(_3586.GearCompoundStabilityAnalysis):
    '''ConceptGearCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2167.ConceptGear':
        '''ConceptGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2167.ConceptGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3427.ConceptGearStabilityAnalysis]':
        '''List[ConceptGearStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3427.ConceptGearStabilityAnalysis))
        return value

    @property
    def component_stability_analysis_load_cases(self) -> 'List[_3427.ConceptGearStabilityAnalysis]':
        '''List[ConceptGearStabilityAnalysis]: 'ComponentStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentStabilityAnalysisLoadCases, constructor.new(_3427.ConceptGearStabilityAnalysis))
        return value

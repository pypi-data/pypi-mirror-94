'''_6353.py

OilSealCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2114
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6224
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6311
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'OilSealCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealCompoundCriticalSpeedAnalysis',)


class OilSealCompoundCriticalSpeedAnalysis(_6311.ConnectorCompoundCriticalSpeedAnalysis):
    '''OilSealCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2114.OilSeal':
        '''OilSeal: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2114.OilSeal)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6224.OilSealCriticalSpeedAnalysis]':
        '''List[OilSealCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6224.OilSealCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6224.OilSealCriticalSpeedAnalysis]':
        '''List[OilSealCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6224.OilSealCriticalSpeedAnalysis))
        return value

'''_6362.py

PowerLoadCompoundCriticalSpeedAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2120
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6233
from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6397
from mastapy._internal.python_net import python_net_import

_POWER_LOAD_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'PowerLoadCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerLoadCompoundCriticalSpeedAnalysis',)


class PowerLoadCompoundCriticalSpeedAnalysis(_6397.VirtualComponentCompoundCriticalSpeedAnalysis):
    '''PowerLoadCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_LOAD_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerLoadCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2120.PowerLoad':
        '''PowerLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2120.PowerLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6233.PowerLoadCriticalSpeedAnalysis]':
        '''List[PowerLoadCriticalSpeedAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6233.PowerLoadCriticalSpeedAnalysis))
        return value

    @property
    def component_critical_speed_analysis_load_cases(self) -> 'List[_6233.PowerLoadCriticalSpeedAnalysis]':
        '''List[PowerLoadCriticalSpeedAnalysis]: 'ComponentCriticalSpeedAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentCriticalSpeedAnalysisLoadCases, constructor.new(_6233.PowerLoadCriticalSpeedAnalysis))
        return value

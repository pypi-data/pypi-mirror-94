'''_6068.py

PointLoadCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2071
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5947
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import _6102
from mastapy._internal.python_net import python_net_import

_POINT_LOAD_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'PointLoadCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PointLoadCompoundDynamicAnalysis',)


class PointLoadCompoundDynamicAnalysis(_6102.VirtualComponentCompoundDynamicAnalysis):
    '''PointLoadCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _POINT_LOAD_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PointLoadCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2071.PointLoad':
        '''PointLoad: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2071.PointLoad)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5947.PointLoadDynamicAnalysis]':
        '''List[PointLoadDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5947.PointLoadDynamicAnalysis))
        return value

    @property
    def component_dynamic_analysis_load_cases(self) -> 'List[_5947.PointLoadDynamicAnalysis]':
        '''List[PointLoadDynamicAnalysis]: 'ComponentDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDynamicAnalysisLoadCases, constructor.new(_5947.PointLoadDynamicAnalysis))
        return value

'''_4981.py

MeasurementComponentCompoundModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2063
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses import _4837
from mastapy.system_model.analyses_and_results.modal_analyses.compound import _5025
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Compound', 'MeasurementComponentCompoundModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentCompoundModalAnalysis',)


class MeasurementComponentCompoundModalAnalysis(_5025.VirtualComponentCompoundModalAnalysis):
    '''MeasurementComponentCompoundModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_COMPOUND_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentCompoundModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2063.MeasurementComponent':
        '''MeasurementComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2063.MeasurementComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4837.MeasurementComponentModalAnalysis]':
        '''List[MeasurementComponentModalAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4837.MeasurementComponentModalAnalysis))
        return value

    @property
    def component_modal_analysis_load_cases(self) -> 'List[_4837.MeasurementComponentModalAnalysis]':
        '''List[MeasurementComponentModalAnalysis]: 'ComponentModalAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentModalAnalysisLoadCases, constructor.new(_4837.MeasurementComponentModalAnalysis))
        return value

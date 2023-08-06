'''_3645.py

TorqueConverterCompoundStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2252
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.stability_analyses import _3518
from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3565
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'TorqueConverterCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterCompoundStabilityAnalysis',)


class TorqueConverterCompoundStabilityAnalysis(_3565.CouplingCompoundStabilityAnalysis):
    '''TorqueConverterCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2252.TorqueConverter':
        '''TorqueConverter: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.TorqueConverter)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2252.TorqueConverter':
        '''TorqueConverter: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2252.TorqueConverter)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_3518.TorqueConverterStabilityAnalysis]':
        '''List[TorqueConverterStabilityAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3518.TorqueConverterStabilityAnalysis))
        return value

    @property
    def assembly_stability_analysis_load_cases(self) -> 'List[_3518.TorqueConverterStabilityAnalysis]':
        '''List[TorqueConverterStabilityAnalysis]: 'AssemblyStabilityAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyStabilityAnalysisLoadCases, constructor.new(_3518.TorqueConverterStabilityAnalysis))
        return value

'''_6664.py

FEPartAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.analyses_and_results.harmonic_analyses import _5641
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _2101
from mastapy.system_model.analyses_and_results.static_loads import _6484
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6606
from mastapy._internal.python_net import python_net_import

_FE_PART_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'FEPartAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('FEPartAdvancedTimeSteppingAnalysisForModulation',)


class FEPartAdvancedTimeSteppingAnalysisForModulation(_6606.AbstractShaftOrHousingAdvancedTimeSteppingAnalysisForModulation):
    '''FEPartAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _FE_PART_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FEPartAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def export(self) -> '_5641.HarmonicAnalysisFEExportOptions':
        '''HarmonicAnalysisFEExportOptions: 'Export' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_5641.HarmonicAnalysisFEExportOptions)(self.wrapped.Export) if self.wrapped.Export else None

    @property
    def component_design(self) -> '_2101.FEPart':
        '''FEPart: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2101.FEPart)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6484.FEPartLoadCase':
        '''FEPartLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6484.FEPartLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def planetaries(self) -> 'List[FEPartAdvancedTimeSteppingAnalysisForModulation]':
        '''List[FEPartAdvancedTimeSteppingAnalysisForModulation]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(FEPartAdvancedTimeSteppingAnalysisForModulation))
        return value

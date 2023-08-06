'''_6687.py

OilSealAdvancedTimeSteppingAnalysisForModulation
'''


from mastapy.system_model.part_model import _2114
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6522
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6644
from mastapy._internal.python_net import python_net_import

_OIL_SEAL_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation', 'OilSealAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('OilSealAdvancedTimeSteppingAnalysisForModulation',)


class OilSealAdvancedTimeSteppingAnalysisForModulation(_6644.ConnectorAdvancedTimeSteppingAnalysisForModulation):
    '''OilSealAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _OIL_SEAL_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilSealAdvancedTimeSteppingAnalysisForModulation.TYPE'):
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
    def component_load_case(self) -> '_6522.OilSealLoadCase':
        '''OilSealLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6522.OilSealLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

'''_6821.py

PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1940
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import _6692
from mastapy.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation.compound import _6835
from mastapy._internal.python_net import python_net_import

_PLANETARY_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation.Compound', 'PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation')


__docformat__ = 'restructuredtext en'
__all__ = ('PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation',)


class PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation(_6835.ShaftToMountableComponentConnectionCompoundAdvancedTimeSteppingAnalysisForModulation):
    '''PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    '''

    TYPE = _PLANETARY_CONNECTION_COMPOUND_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlanetaryConnectionCompoundAdvancedTimeSteppingAnalysisForModulation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1940.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1940.PlanetaryConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1940.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1940.PlanetaryConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_6692.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6692.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value

    @property
    def connection_advanced_time_stepping_analysis_for_modulation_load_cases(self) -> 'List[_6692.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation]':
        '''List[PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation]: 'ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionAdvancedTimeSteppingAnalysisForModulationLoadCases, constructor.new(_6692.PlanetaryConnectionAdvancedTimeSteppingAnalysisForModulation))
        return value

'''_4377.py

CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _1990
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4247
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4334
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness',)


class CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness(_4334.AbstractShaftToMountableComponentConnectionCompoundModalAnalysisAtAStiffness):
    '''CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscPlanetaryBearingConnectionCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1990.CycloidalDiscPlanetaryBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_4247.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness]':
        '''List[CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4247.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def connection_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4247.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness]':
        '''List[CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness]: 'ConnectionModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionModalAnalysisAtAStiffnessLoadCases, constructor.new(_4247.CycloidalDiscPlanetaryBearingConnectionModalAnalysisAtAStiffness))
        return value

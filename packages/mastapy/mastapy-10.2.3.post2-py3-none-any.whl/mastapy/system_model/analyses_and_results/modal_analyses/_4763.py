'''_4763.py

CycloidalDiscCentralBearingConnectionModalAnalysis
'''


from mastapy.system_model.connections_and_sockets.cycloidal import _1987
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2371
from mastapy.system_model.analyses_and_results.modal_analyses import _4742
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'CycloidalDiscCentralBearingConnectionModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalDiscCentralBearingConnectionModalAnalysis',)


class CycloidalDiscCentralBearingConnectionModalAnalysis(_4742.CoaxialConnectionModalAnalysis):
    '''CycloidalDiscCentralBearingConnectionModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalDiscCentralBearingConnectionModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1987.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1987.CycloidalDiscCentralBearingConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def system_deflection_results(self) -> '_2371.CycloidalDiscCentralBearingConnectionSystemDeflection':
        '''CycloidalDiscCentralBearingConnectionSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2371.CycloidalDiscCentralBearingConnectionSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

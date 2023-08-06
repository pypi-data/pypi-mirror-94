'''_3516.py

TorqueConverterConnectionStabilityAnalysis
'''


from mastapy.system_model.connections_and_sockets.couplings import _2004
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6571
from mastapy.system_model.analyses_and_results.stability_analyses import _3433
from mastapy._internal.python_net import python_net_import

_TORQUE_CONVERTER_CONNECTION_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'TorqueConverterConnectionStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('TorqueConverterConnectionStabilityAnalysis',)


class TorqueConverterConnectionStabilityAnalysis(_3433.CouplingConnectionStabilityAnalysis):
    '''TorqueConverterConnectionStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _TORQUE_CONVERTER_CONNECTION_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'TorqueConverterConnectionStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_2004.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2004.TorqueConverterConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6571.TorqueConverterConnectionLoadCase':
        '''TorqueConverterConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6571.TorqueConverterConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

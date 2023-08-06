'''_5113.py

MeasurementComponentMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model import _2063
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6219
from mastapy.system_model.analyses_and_results.mbd_analyses import _5163
from mastapy._internal.python_net import python_net_import

_MEASUREMENT_COMPONENT_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'MeasurementComponentMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('MeasurementComponentMultiBodyDynamicsAnalysis',)


class MeasurementComponentMultiBodyDynamicsAnalysis(_5163.VirtualComponentMultiBodyDynamicsAnalysis):
    '''MeasurementComponentMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _MEASUREMENT_COMPONENT_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'MeasurementComponentMultiBodyDynamicsAnalysis.TYPE'):
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
    def component_load_case(self) -> '_6219.MeasurementComponentLoadCase':
        '''MeasurementComponentLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6219.MeasurementComponentLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

'''_3253.py

SynchroniserSleeveSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model.couplings import _2251
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6568
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3252
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'SynchroniserSleeveSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveSteadyStateSynchronousResponse',)


class SynchroniserSleeveSteadyStateSynchronousResponse(_3252.SynchroniserPartSteadyStateSynchronousResponse):
    '''SynchroniserSleeveSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2251.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2251.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6568.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6568.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

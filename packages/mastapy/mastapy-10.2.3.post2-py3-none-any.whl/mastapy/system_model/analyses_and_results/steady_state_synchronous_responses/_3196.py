'''_3196.py

GuideDxfModelSteadyStateSynchronousResponse
'''


from mastapy.system_model.part_model import _2103
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6493
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses import _3159
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponses', 'GuideDxfModelSteadyStateSynchronousResponse')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelSteadyStateSynchronousResponse',)


class GuideDxfModelSteadyStateSynchronousResponse(_3159.ComponentSteadyStateSynchronousResponse):
    '''GuideDxfModelSteadyStateSynchronousResponse

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_STEADY_STATE_SYNCHRONOUS_RESPONSE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelSteadyStateSynchronousResponse.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2103.GuideDxfModel':
        '''GuideDxfModel: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2103.GuideDxfModel)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6493.GuideDxfModelLoadCase':
        '''GuideDxfModelLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6493.GuideDxfModelLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

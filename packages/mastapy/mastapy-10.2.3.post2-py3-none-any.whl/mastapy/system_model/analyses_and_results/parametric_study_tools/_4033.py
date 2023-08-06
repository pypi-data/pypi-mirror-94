'''_4033.py

RingPinsToDiscConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets.cycloidal import _1993
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6540
from mastapy.system_model.analyses_and_results.system_deflections import _2428
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3997
from mastapy._internal.python_net import python_net_import

_RING_PINS_TO_DISC_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'RingPinsToDiscConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('RingPinsToDiscConnectionParametricStudyTool',)


class RingPinsToDiscConnectionParametricStudyTool(_3997.InterMountableComponentConnectionParametricStudyTool):
    '''RingPinsToDiscConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _RING_PINS_TO_DISC_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RingPinsToDiscConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def connection_design(self) -> '_1993.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1993.RingPinsToDiscConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6540.RingPinsToDiscConnectionLoadCase':
        '''RingPinsToDiscConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6540.RingPinsToDiscConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2428.RingPinsToDiscConnectionSystemDeflection]':
        '''List[RingPinsToDiscConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2428.RingPinsToDiscConnectionSystemDeflection))
        return value

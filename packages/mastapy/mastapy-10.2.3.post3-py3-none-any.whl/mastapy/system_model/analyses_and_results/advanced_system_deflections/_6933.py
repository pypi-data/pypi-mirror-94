'''_6933.py

GuideDxfModelAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _2103
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6493
from mastapy.system_model.analyses_and_results.system_deflections import _2395
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6895
from mastapy._internal.python_net import python_net_import

_GUIDE_DXF_MODEL_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'GuideDxfModelAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('GuideDxfModelAdvancedSystemDeflection',)


class GuideDxfModelAdvancedSystemDeflection(_6895.ComponentAdvancedSystemDeflection):
    '''GuideDxfModelAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _GUIDE_DXF_MODEL_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GuideDxfModelAdvancedSystemDeflection.TYPE'):
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

    @property
    def component_system_deflection_results(self) -> 'List[_2395.GuideDxfModelSystemDeflection]':
        '''List[GuideDxfModelSystemDeflection]: 'ComponentSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentSystemDeflectionResults, constructor.new(_2395.GuideDxfModelSystemDeflection))
        return value

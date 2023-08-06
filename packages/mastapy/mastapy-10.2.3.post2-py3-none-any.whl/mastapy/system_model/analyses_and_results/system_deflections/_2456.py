'''_2456.py

SynchroniserSleeveSystemDeflection
'''


from mastapy.system_model.part_model.couplings import _2251
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6568
from mastapy.system_model.analyses_and_results.power_flows import _3782
from mastapy.system_model.analyses_and_results.system_deflections import _2455
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'SynchroniserSleeveSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveSystemDeflection',)


class SynchroniserSleeveSystemDeflection(_2455.SynchroniserPartSystemDeflection):
    '''SynchroniserSleeveSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveSystemDeflection.TYPE'):
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

    @property
    def power_flow_results(self) -> '_3782.SynchroniserSleevePowerFlow':
        '''SynchroniserSleevePowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3782.SynchroniserSleevePowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

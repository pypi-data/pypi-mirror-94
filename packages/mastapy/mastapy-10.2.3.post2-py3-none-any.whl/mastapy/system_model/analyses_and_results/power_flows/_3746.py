'''_3746.py

PartToPartShearCouplingPowerFlow
'''


from mastapy.system_model.part_model.couplings import _2234
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6527
from mastapy.system_model.analyses_and_results.power_flows import _3702
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'PartToPartShearCouplingPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingPowerFlow',)


class PartToPartShearCouplingPowerFlow(_3702.CouplingPowerFlow):
    '''PartToPartShearCouplingPowerFlow

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2234.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2234.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6527.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6527.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

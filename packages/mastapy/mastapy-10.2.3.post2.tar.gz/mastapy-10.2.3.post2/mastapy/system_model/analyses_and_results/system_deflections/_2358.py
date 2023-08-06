'''_2358.py

PartToPartShearCouplingSystemDeflection
'''


from mastapy.system_model.analyses_and_results.system_deflections import _2356, _2308
from mastapy._internal import constructor
from mastapy.system_model.part_model.couplings import _2182
from mastapy.system_model.analyses_and_results.static_loads import _6228
from mastapy.system_model.analyses_and_results.power_flows import _3357
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'PartToPartShearCouplingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingSystemDeflection',)


class PartToPartShearCouplingSystemDeflection(_2308.CouplingSystemDeflection):
    '''PartToPartShearCouplingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def part_to_part_shear_coupling_connection(self) -> '_2356.PartToPartShearCouplingConnectionSystemDeflection':
        '''PartToPartShearCouplingConnectionSystemDeflection: 'PartToPartShearCouplingConnection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2356.PartToPartShearCouplingConnectionSystemDeflection)(self.wrapped.PartToPartShearCouplingConnection) if self.wrapped.PartToPartShearCouplingConnection else None

    @property
    def assembly_design(self) -> '_2182.PartToPartShearCoupling':
        '''PartToPartShearCoupling: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2182.PartToPartShearCoupling)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6228.PartToPartShearCouplingLoadCase':
        '''PartToPartShearCouplingLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6228.PartToPartShearCouplingLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def power_flow_results(self) -> '_3357.PartToPartShearCouplingPowerFlow':
        '''PartToPartShearCouplingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3357.PartToPartShearCouplingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

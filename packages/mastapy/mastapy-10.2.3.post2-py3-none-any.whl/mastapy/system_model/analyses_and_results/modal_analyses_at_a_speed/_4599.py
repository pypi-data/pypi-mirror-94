'''_4599.py

PartToPartShearCouplingModalAnalysisAtASpeed
'''


from mastapy.system_model.part_model.couplings import _2182
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6228
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4559
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed', 'PartToPartShearCouplingModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCouplingModalAnalysisAtASpeed',)


class PartToPartShearCouplingModalAnalysisAtASpeed(_4559.CouplingModalAnalysisAtASpeed):
    '''PartToPartShearCouplingModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCouplingModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

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

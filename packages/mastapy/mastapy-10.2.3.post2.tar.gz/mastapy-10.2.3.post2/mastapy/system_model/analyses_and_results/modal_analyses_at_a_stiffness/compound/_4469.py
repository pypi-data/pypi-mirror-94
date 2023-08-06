'''_4469.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model.gears import _2139
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness.compound import _4467, _4468, _4463
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4347
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness(_4463.KlingelnbergCycloPalloidConicalGearSetCompoundModalAnalysisAtAStiffness):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2139.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2139.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2139.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4467.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundModalAnalysisAtAStiffness, constructor.new(_4467.KlingelnbergCycloPalloidSpiralBevelGearCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_modal_analysis_at_a_stiffness(self) -> 'List[_4468.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysisAtAStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundModalAnalysisAtAStiffness, constructor.new(_4468.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundModalAnalysisAtAStiffness))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4347.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4347.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def assembly_modal_analysis_at_a_stiffness_load_cases(self) -> 'List[_4347.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]: 'AssemblyModalAnalysisAtAStiffnessLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtAStiffnessLoadCases, constructor.new(_4347.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

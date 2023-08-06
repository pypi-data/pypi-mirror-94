'''_5270.py

SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2142
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5268, _5269, _5193
from mastapy.system_model.analyses_and_results.mbd_analyses import _5140
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis',)


class SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis(_5193.BevelGearSetCompoundMultiBodyDynamicsAnalysis):
    '''SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2142.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.SpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2142.SpiralBevelGearSet':
        '''SpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2142.SpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def spiral_bevel_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5268.SpiralBevelGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearCompoundMultiBodyDynamicsAnalysis]: 'SpiralBevelGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5268.SpiralBevelGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5269.SpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis]: 'SpiralBevelMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5269.SpiralBevelGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5140.SpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5140.SpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5140.SpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5140.SpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

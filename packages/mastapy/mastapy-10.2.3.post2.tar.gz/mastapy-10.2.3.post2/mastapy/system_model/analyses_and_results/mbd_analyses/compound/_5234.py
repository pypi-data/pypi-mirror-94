'''_5234.py

HypoidGearSetCompoundMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2133
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.mbd_analyses.compound import _5232, _5233, _5181
from mastapy.system_model.analyses_and_results.mbd_analyses import _5093
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses.Compound', 'HypoidGearSetCompoundMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetCompoundMultiBodyDynamicsAnalysis',)


class HypoidGearSetCompoundMultiBodyDynamicsAnalysis(_5181.AGMAGleasonConicalGearSetCompoundMultiBodyDynamicsAnalysis):
    '''HypoidGearSetCompoundMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_COMPOUND_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetCompoundMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2133.HypoidGearSet':
        '''HypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.HypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2133.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def hypoid_gears_compound_multi_body_dynamics_analysis(self) -> 'List[_5232.HypoidGearCompoundMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearCompoundMultiBodyDynamicsAnalysis]: 'HypoidGearsCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsCompoundMultiBodyDynamicsAnalysis, constructor.new(_5232.HypoidGearCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_meshes_compound_multi_body_dynamics_analysis(self) -> 'List[_5233.HypoidGearMeshCompoundMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearMeshCompoundMultiBodyDynamicsAnalysis]: 'HypoidMeshesCompoundMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesCompoundMultiBodyDynamicsAnalysis, constructor.new(_5233.HypoidGearMeshCompoundMultiBodyDynamicsAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5093.HypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultiBodyDynamicsAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5093.HypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def assembly_multi_body_dynamics_analysis_load_cases(self) -> 'List[_5093.HypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultiBodyDynamicsAnalysis]: 'AssemblyMultiBodyDynamicsAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyMultiBodyDynamicsAnalysisLoadCases, constructor.new(_5093.HypoidGearSetMultiBodyDynamicsAnalysis))
        return value

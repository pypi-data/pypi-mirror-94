'''_5924.py

HypoidGearSetDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2133
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6205
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5922, _5923, _5869
from mastapy._internal.python_net import python_net_import

_HYPOID_GEAR_SET_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses', 'HypoidGearSetDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('HypoidGearSetDynamicAnalysis',)


class HypoidGearSetDynamicAnalysis(_5869.AGMAGleasonConicalGearSetDynamicAnalysis):
    '''HypoidGearSetDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _HYPOID_GEAR_SET_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HypoidGearSetDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2133.HypoidGearSet':
        '''HypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2133.HypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6205.HypoidGearSetLoadCase':
        '''HypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6205.HypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def hypoid_gears_dynamic_analysis(self) -> 'List[_5922.HypoidGearDynamicAnalysis]':
        '''List[HypoidGearDynamicAnalysis]: 'HypoidGearsDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearsDynamicAnalysis, constructor.new(_5922.HypoidGearDynamicAnalysis))
        return value

    @property
    def hypoid_meshes_dynamic_analysis(self) -> 'List[_5923.HypoidGearMeshDynamicAnalysis]':
        '''List[HypoidGearMeshDynamicAnalysis]: 'HypoidMeshesDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidMeshesDynamicAnalysis, constructor.new(_5923.HypoidGearMeshDynamicAnalysis))
        return value

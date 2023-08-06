'''_3426.py

ConceptGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2168
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6441
from mastapy.system_model.analyses_and_results.stability_analyses import _3427, _3425, _3456
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'ConceptGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetStabilityAnalysis',)


class ConceptGearSetStabilityAnalysis(_3456.GearSetStabilityAnalysis):
    '''ConceptGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2168.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2168.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6441.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6441.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def concept_gears_stability_analysis(self) -> 'List[_3427.ConceptGearStabilityAnalysis]':
        '''List[ConceptGearStabilityAnalysis]: 'ConceptGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsStabilityAnalysis, constructor.new(_3427.ConceptGearStabilityAnalysis))
        return value

    @property
    def concept_meshes_stability_analysis(self) -> 'List[_3425.ConceptGearMeshStabilityAnalysis]':
        '''List[ConceptGearMeshStabilityAnalysis]: 'ConceptMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesStabilityAnalysis, constructor.new(_3425.ConceptGearMeshStabilityAnalysis))
        return value

'''_3508.py

StraightBevelGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2194
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6562
from mastapy.system_model.analyses_and_results.stability_analyses import _3509, _3507, _3413
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'StraightBevelGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetStabilityAnalysis',)


class StraightBevelGearSetStabilityAnalysis(_3413.BevelGearSetStabilityAnalysis):
    '''StraightBevelGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2194.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2194.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6562.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6562.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_stability_analysis(self) -> 'List[_3509.StraightBevelGearStabilityAnalysis]':
        '''List[StraightBevelGearStabilityAnalysis]: 'StraightBevelGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsStabilityAnalysis, constructor.new(_3509.StraightBevelGearStabilityAnalysis))
        return value

    @property
    def straight_bevel_meshes_stability_analysis(self) -> 'List[_3507.StraightBevelGearMeshStabilityAnalysis]':
        '''List[StraightBevelGearMeshStabilityAnalysis]: 'StraightBevelMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesStabilityAnalysis, constructor.new(_3507.StraightBevelGearMeshStabilityAnalysis))
        return value

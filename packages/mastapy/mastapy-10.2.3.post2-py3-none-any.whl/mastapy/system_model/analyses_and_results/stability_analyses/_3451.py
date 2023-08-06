'''_3451.py

FaceGearSetStabilityAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2175
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6483
from mastapy.system_model.analyses_and_results.stability_analyses import _3452, _3450, _3456
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_SET_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'FaceGearSetStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearSetStabilityAnalysis',)


class FaceGearSetStabilityAnalysis(_3456.GearSetStabilityAnalysis):
    '''FaceGearSetStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_SET_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearSetStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2175.FaceGearSet':
        '''FaceGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.FaceGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6483.FaceGearSetLoadCase':
        '''FaceGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6483.FaceGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def face_gears_stability_analysis(self) -> 'List[_3452.FaceGearStabilityAnalysis]':
        '''List[FaceGearStabilityAnalysis]: 'FaceGearsStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearsStabilityAnalysis, constructor.new(_3452.FaceGearStabilityAnalysis))
        return value

    @property
    def face_meshes_stability_analysis(self) -> 'List[_3450.FaceGearMeshStabilityAnalysis]':
        '''List[FaceGearMeshStabilityAnalysis]: 'FaceMeshesStabilityAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceMeshesStabilityAnalysis, constructor.new(_3450.FaceGearMeshStabilityAnalysis))
        return value

'''_5078.py

CylindricalGearSetMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2124, _2140
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6165, _6230
from mastapy.system_model.analyses_and_results.mbd_analyses import _5077, _5076, _5089
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CylindricalGearSetMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetMultiBodyDynamicsAnalysis',)


class CylindricalGearSetMultiBodyDynamicsAnalysis(_5089.GearSetMultiBodyDynamicsAnalysis):
    '''CylindricalGearSetMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2124.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2124.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6165.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6165.CylindricalGearSetLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to CylindricalGearSetLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def gears(self) -> 'List[_5077.CylindricalGearMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMultiBodyDynamicsAnalysis]: 'Gears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Gears, constructor.new(_5077.CylindricalGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gears_multi_body_dynamics_analysis(self) -> 'List[_5077.CylindricalGearMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMultiBodyDynamicsAnalysis]: 'CylindricalGearsMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsMultiBodyDynamicsAnalysis, constructor.new(_5077.CylindricalGearMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_meshes_multi_body_dynamics_analysis(self) -> 'List[_5076.CylindricalGearMeshMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearMeshMultiBodyDynamicsAnalysis]: 'CylindricalMeshesMultiBodyDynamicsAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesMultiBodyDynamicsAnalysis, constructor.new(_5076.CylindricalGearMeshMultiBodyDynamicsAnalysis))
        return value

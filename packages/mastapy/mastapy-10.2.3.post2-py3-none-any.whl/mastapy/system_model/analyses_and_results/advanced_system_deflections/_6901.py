'''_6901.py

ConceptGearSetAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model.gears import _2168
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6441
from mastapy.gears.rating.concept import _500
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6899, _6900, _6932
from mastapy.system_model.analyses_and_results.system_deflections import _2356
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'ConceptGearSetAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetAdvancedSystemDeflection',)


class ConceptGearSetAdvancedSystemDeflection(_6932.GearSetAdvancedSystemDeflection):
    '''ConceptGearSetAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetAdvancedSystemDeflection.TYPE'):
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
    def rating(self) -> '_500.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_500.ConceptGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_500.ConceptGearSetRating':
        '''ConceptGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_500.ConceptGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def concept_gears_advanced_system_deflection(self) -> 'List[_6899.ConceptGearAdvancedSystemDeflection]':
        '''List[ConceptGearAdvancedSystemDeflection]: 'ConceptGearsAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsAdvancedSystemDeflection, constructor.new(_6899.ConceptGearAdvancedSystemDeflection))
        return value

    @property
    def concept_meshes_advanced_system_deflection(self) -> 'List[_6900.ConceptGearMeshAdvancedSystemDeflection]':
        '''List[ConceptGearMeshAdvancedSystemDeflection]: 'ConceptMeshesAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesAdvancedSystemDeflection, constructor.new(_6900.ConceptGearMeshAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2356.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2356.ConceptGearSetSystemDeflection))
        return value

'''_4832.py

KlingelnbergCycloPalloidHypoidGearSetModalAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2137
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6214
from mastapy.system_model.analyses_and_results.system_deflections import _2342
from mastapy.system_model.analyses_and_results.modal_analyses import _4831, _4830, _4829
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetModalAnalysis',)


class KlingelnbergCycloPalloidHypoidGearSetModalAnalysis(_4829.KlingelnbergCycloPalloidConicalGearSetModalAnalysis):
    '''KlingelnbergCycloPalloidHypoidGearSetModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2137.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2137.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6214.KlingelnbergCycloPalloidHypoidGearSetLoadCase':
        '''KlingelnbergCycloPalloidHypoidGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6214.KlingelnbergCycloPalloidHypoidGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2342.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2342.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_modal_analysis(self) -> 'List[_4831.KlingelnbergCycloPalloidHypoidGearModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearsModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsModalAnalysis, constructor.new(_4831.KlingelnbergCycloPalloidHypoidGearModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_modal_analysis(self) -> 'List[_4830.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis]: 'KlingelnbergCycloPalloidHypoidMeshesModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesModalAnalysis, constructor.new(_4830.KlingelnbergCycloPalloidHypoidGearMeshModalAnalysis))
        return value

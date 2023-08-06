'''_3867.py

KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2185
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.power_flows.compound import _3865, _3866, _3864
from mastapy.system_model.analyses_and_results.power_flows import _3735
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow',)


class KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow(_3864.KlingelnbergCycloPalloidConicalGearSetCompoundPowerFlow):
    '''KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidHypoidGearSetCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2185.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2185.KlingelnbergCycloPalloidHypoidGearSet':
        '''KlingelnbergCycloPalloidHypoidGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2185.KlingelnbergCycloPalloidHypoidGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_hypoid_gears_compound_power_flow(self) -> 'List[_3865.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow]: 'KlingelnbergCycloPalloidHypoidGearsCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearsCompoundPowerFlow, constructor.new(_3865.KlingelnbergCycloPalloidHypoidGearCompoundPowerFlow))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_meshes_compound_power_flow(self) -> 'List[_3866.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow]: 'KlingelnbergCycloPalloidHypoidMeshesCompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidMeshesCompoundPowerFlow, constructor.new(_3866.KlingelnbergCycloPalloidHypoidGearMeshCompoundPowerFlow))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_3735.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetPowerFlow]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3735.KlingelnbergCycloPalloidHypoidGearSetPowerFlow))
        return value

    @property
    def assembly_power_flow_load_cases(self) -> 'List[_3735.KlingelnbergCycloPalloidHypoidGearSetPowerFlow]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetPowerFlow]: 'AssemblyPowerFlowLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyPowerFlowLoadCases, constructor.new(_3735.KlingelnbergCycloPalloidHypoidGearSetPowerFlow))
        return value

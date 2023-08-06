'''_4283.py

AssemblyModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _2037, _2074
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6123, _6242
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _4284, _4286, _4289, _4296,
    _4295, _4299, _4304, _4307,
    _4317, _4321, _4328, _4329,
    _4336, _4337, _4344, _4347,
    _4348, _4349, _4352, _4356,
    _4359, _4360, _4361, _4367,
    _4363, _4368, _4373, _4376,
    _4379, _4382, _4386, _4390,
    _4393, _4397, _4400, _4278
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'AssemblyModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysisAtAStiffness',)


class AssemblyModalAnalysisAtAStiffness(_4278.AbstractAssemblyModalAnalysisAtAStiffness):
    '''AssemblyModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2037.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2037.Assembly.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to Assembly. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6123.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6123.AssemblyLoadCase.TYPE not in self.wrapped.AssemblyLoadCase.__class__.__mro__:
            raise CastException('Failed to cast assembly_load_case to AssemblyLoadCase. Expected: {}.'.format(self.wrapped.AssemblyLoadCase.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyLoadCase.__class__)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_4284.BearingModalAnalysisAtAStiffness]':
        '''List[BearingModalAnalysisAtAStiffness]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4284.BearingModalAnalysisAtAStiffness))
        return value

    @property
    def belt_drives(self) -> 'List[_4286.BeltDriveModalAnalysisAtAStiffness]':
        '''List[BeltDriveModalAnalysisAtAStiffness]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4286.BeltDriveModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4289.BevelDifferentialGearSetModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetModalAnalysisAtAStiffness]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4289.BevelDifferentialGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def bolts(self) -> 'List[_4296.BoltModalAnalysisAtAStiffness]':
        '''List[BoltModalAnalysisAtAStiffness]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4296.BoltModalAnalysisAtAStiffness))
        return value

    @property
    def bolted_joints(self) -> 'List[_4295.BoltedJointModalAnalysisAtAStiffness]':
        '''List[BoltedJointModalAnalysisAtAStiffness]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4295.BoltedJointModalAnalysisAtAStiffness))
        return value

    @property
    def clutches(self) -> 'List[_4299.ClutchModalAnalysisAtAStiffness]':
        '''List[ClutchModalAnalysisAtAStiffness]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4299.ClutchModalAnalysisAtAStiffness))
        return value

    @property
    def concept_couplings(self) -> 'List[_4304.ConceptCouplingModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingModalAnalysisAtAStiffness]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4304.ConceptCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4307.ConceptGearSetModalAnalysisAtAStiffness]':
        '''List[ConceptGearSetModalAnalysisAtAStiffness]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4307.ConceptGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def cv_ts(self) -> 'List[_4317.CVTModalAnalysisAtAStiffness]':
        '''List[CVTModalAnalysisAtAStiffness]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4317.CVTModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4321.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4321.CylindricalGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4328.FaceGearSetModalAnalysisAtAStiffness]':
        '''List[FaceGearSetModalAnalysisAtAStiffness]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4328.FaceGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4329.FlexiblePinAssemblyModalAnalysisAtAStiffness]':
        '''List[FlexiblePinAssemblyModalAnalysisAtAStiffness]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4329.FlexiblePinAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4336.HypoidGearSetModalAnalysisAtAStiffness]':
        '''List[HypoidGearSetModalAnalysisAtAStiffness]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4336.HypoidGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4337.ImportedFEComponentModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentModalAnalysisAtAStiffness]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4337.ImportedFEComponentModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4344.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4344.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4347.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4347.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def mass_discs(self) -> 'List[_4348.MassDiscModalAnalysisAtAStiffness]':
        '''List[MassDiscModalAnalysisAtAStiffness]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4348.MassDiscModalAnalysisAtAStiffness))
        return value

    @property
    def measurement_components(self) -> 'List[_4349.MeasurementComponentModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentModalAnalysisAtAStiffness]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4349.MeasurementComponentModalAnalysisAtAStiffness))
        return value

    @property
    def oil_seals(self) -> 'List[_4352.OilSealModalAnalysisAtAStiffness]':
        '''List[OilSealModalAnalysisAtAStiffness]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4352.OilSealModalAnalysisAtAStiffness))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4356.PartToPartShearCouplingModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingModalAnalysisAtAStiffness]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4356.PartToPartShearCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def planet_carriers(self) -> 'List[_4359.PlanetCarrierModalAnalysisAtAStiffness]':
        '''List[PlanetCarrierModalAnalysisAtAStiffness]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4359.PlanetCarrierModalAnalysisAtAStiffness))
        return value

    @property
    def point_loads(self) -> 'List[_4360.PointLoadModalAnalysisAtAStiffness]':
        '''List[PointLoadModalAnalysisAtAStiffness]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4360.PointLoadModalAnalysisAtAStiffness))
        return value

    @property
    def power_loads(self) -> 'List[_4361.PowerLoadModalAnalysisAtAStiffness]':
        '''List[PowerLoadModalAnalysisAtAStiffness]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4361.PowerLoadModalAnalysisAtAStiffness))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4367.ShaftHubConnectionModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionModalAnalysisAtAStiffness]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4367.ShaftHubConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4363.RollingRingAssemblyModalAnalysisAtAStiffness]':
        '''List[RollingRingAssemblyModalAnalysisAtAStiffness]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4363.RollingRingAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def shafts(self) -> 'List[_4368.ShaftModalAnalysisAtAStiffness]':
        '''List[ShaftModalAnalysisAtAStiffness]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4368.ShaftModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4373.SpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearSetModalAnalysisAtAStiffness]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4373.SpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def spring_dampers(self) -> 'List[_4376.SpringDamperModalAnalysisAtAStiffness]':
        '''List[SpringDamperModalAnalysisAtAStiffness]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4376.SpringDamperModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4379.StraightBevelDiffGearSetModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearSetModalAnalysisAtAStiffness]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4379.StraightBevelDiffGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4382.StraightBevelGearSetModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearSetModalAnalysisAtAStiffness]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4382.StraightBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def synchronisers(self) -> 'List[_4386.SynchroniserModalAnalysisAtAStiffness]':
        '''List[SynchroniserModalAnalysisAtAStiffness]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4386.SynchroniserModalAnalysisAtAStiffness))
        return value

    @property
    def torque_converters(self) -> 'List[_4390.TorqueConverterModalAnalysisAtAStiffness]':
        '''List[TorqueConverterModalAnalysisAtAStiffness]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4390.TorqueConverterModalAnalysisAtAStiffness))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4393.UnbalancedMassModalAnalysisAtAStiffness]':
        '''List[UnbalancedMassModalAnalysisAtAStiffness]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4393.UnbalancedMassModalAnalysisAtAStiffness))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4397.WormGearSetModalAnalysisAtAStiffness]':
        '''List[WormGearSetModalAnalysisAtAStiffness]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4397.WormGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4400.ZerolBevelGearSetModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetModalAnalysisAtAStiffness]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4400.ZerolBevelGearSetModalAnalysisAtAStiffness))
        return value

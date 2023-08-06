'''_5038.py

AssemblyMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _2037, _2074
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.static_loads import _6123, _6242
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5039, _5042, _5045, _5052,
    _5051, _5055, _5061, _5064,
    _5074, _5078, _5084, _5085,
    _5093, _5094, _5105, _5108,
    _5109, _5113, _5116, _5120,
    _5123, _5124, _5125, _5133,
    _5127, _5134, _5140, _5143,
    _5146, _5149, _5153, _5158,
    _5162, _5167, _5170, _5099,
    _5033, _5089, _5032
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'AssemblyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyMultiBodyDynamicsAnalysis',)


class AssemblyMultiBodyDynamicsAnalysis(_5032.AbstractAssemblyMultiBodyDynamicsAnalysis):
    '''AssemblyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyMultiBodyDynamicsAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_5039.BearingMultiBodyDynamicsAnalysis]':
        '''List[BearingMultiBodyDynamicsAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5039.BearingMultiBodyDynamicsAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5042.BeltDriveMultiBodyDynamicsAnalysis]':
        '''List[BeltDriveMultiBodyDynamicsAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5042.BeltDriveMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5045.BevelDifferentialGearSetMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetMultiBodyDynamicsAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5045.BevelDifferentialGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5052.BoltMultiBodyDynamicsAnalysis]':
        '''List[BoltMultiBodyDynamicsAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5052.BoltMultiBodyDynamicsAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5051.BoltedJointMultiBodyDynamicsAnalysis]':
        '''List[BoltedJointMultiBodyDynamicsAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5051.BoltedJointMultiBodyDynamicsAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5055.ClutchMultiBodyDynamicsAnalysis]':
        '''List[ClutchMultiBodyDynamicsAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5055.ClutchMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5061.ConceptCouplingMultiBodyDynamicsAnalysis]':
        '''List[ConceptCouplingMultiBodyDynamicsAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5061.ConceptCouplingMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5064.ConceptGearSetMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearSetMultiBodyDynamicsAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5064.ConceptGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5074.CVTMultiBodyDynamicsAnalysis]':
        '''List[CVTMultiBodyDynamicsAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5074.CVTMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5078.CylindricalGearSetMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearSetMultiBodyDynamicsAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5078.CylindricalGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5084.FaceGearSetMultiBodyDynamicsAnalysis]':
        '''List[FaceGearSetMultiBodyDynamicsAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5084.FaceGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5085.FlexiblePinAssemblyMultiBodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultiBodyDynamicsAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5085.FlexiblePinAssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5093.HypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultiBodyDynamicsAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5093.HypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5094.ImportedFEComponentMultiBodyDynamicsAnalysis]':
        '''List[ImportedFEComponentMultiBodyDynamicsAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5094.ImportedFEComponentMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5105.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5105.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5108.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5108.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5109.MassDiscMultiBodyDynamicsAnalysis]':
        '''List[MassDiscMultiBodyDynamicsAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5109.MassDiscMultiBodyDynamicsAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5113.MeasurementComponentMultiBodyDynamicsAnalysis]':
        '''List[MeasurementComponentMultiBodyDynamicsAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5113.MeasurementComponentMultiBodyDynamicsAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5116.OilSealMultiBodyDynamicsAnalysis]':
        '''List[OilSealMultiBodyDynamicsAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5116.OilSealMultiBodyDynamicsAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5120.PartToPartShearCouplingMultiBodyDynamicsAnalysis]':
        '''List[PartToPartShearCouplingMultiBodyDynamicsAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5120.PartToPartShearCouplingMultiBodyDynamicsAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5123.PlanetCarrierMultiBodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultiBodyDynamicsAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5123.PlanetCarrierMultiBodyDynamicsAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5124.PointLoadMultiBodyDynamicsAnalysis]':
        '''List[PointLoadMultiBodyDynamicsAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5124.PointLoadMultiBodyDynamicsAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5125.PowerLoadMultiBodyDynamicsAnalysis]':
        '''List[PowerLoadMultiBodyDynamicsAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5125.PowerLoadMultiBodyDynamicsAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5133.ShaftHubConnectionMultiBodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionMultiBodyDynamicsAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5133.ShaftHubConnectionMultiBodyDynamicsAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5127.RollingRingAssemblyMultiBodyDynamicsAnalysis]':
        '''List[RollingRingAssemblyMultiBodyDynamicsAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5127.RollingRingAssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5134.ShaftMultiBodyDynamicsAnalysis]':
        '''List[ShaftMultiBodyDynamicsAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5134.ShaftMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5140.SpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5140.SpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5143.SpringDamperMultiBodyDynamicsAnalysis]':
        '''List[SpringDamperMultiBodyDynamicsAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5143.SpringDamperMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5146.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5146.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5149.StraightBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultiBodyDynamicsAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5149.StraightBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5153.SynchroniserMultiBodyDynamicsAnalysis]':
        '''List[SynchroniserMultiBodyDynamicsAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5153.SynchroniserMultiBodyDynamicsAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5158.TorqueConverterMultiBodyDynamicsAnalysis]':
        '''List[TorqueConverterMultiBodyDynamicsAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5158.TorqueConverterMultiBodyDynamicsAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5162.UnbalancedMassMultiBodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultiBodyDynamicsAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5162.UnbalancedMassMultiBodyDynamicsAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5167.WormGearSetMultiBodyDynamicsAnalysis]':
        '''List[WormGearSetMultiBodyDynamicsAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5167.WormGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5170.ZerolBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultiBodyDynamicsAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5170.ZerolBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def connections(self) -> 'List[_5099.InterMountableComponentConnectionMultiBodyDynamicsAnalysis]':
        '''List[InterMountableComponentConnectionMultiBodyDynamicsAnalysis]: 'Connections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Connections, constructor.new(_5099.InterMountableComponentConnectionMultiBodyDynamicsAnalysis))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_5033.AbstractShaftOrHousingMultiBodyDynamicsAnalysis]':
        '''List[AbstractShaftOrHousingMultiBodyDynamicsAnalysis]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_5033.AbstractShaftOrHousingMultiBodyDynamicsAnalysis))
        return value

    @property
    def gear_sets(self) -> 'List[_5089.GearSetMultiBodyDynamicsAnalysis]':
        '''List[GearSetMultiBodyDynamicsAnalysis]: 'GearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSets, constructor.new(_5089.GearSetMultiBodyDynamicsAnalysis))
        return value

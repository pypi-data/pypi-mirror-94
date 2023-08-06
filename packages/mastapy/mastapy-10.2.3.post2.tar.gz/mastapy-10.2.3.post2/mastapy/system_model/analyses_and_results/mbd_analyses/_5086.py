'''_5086.py

GearMeshMultiBodyDynamicsAnalysis
'''


from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.nodal_analysis import _1394
from mastapy.system_model.connections_and_sockets.gears import (
    _1930, _1916, _1918, _1920,
    _1922, _1924, _1926, _1928,
    _1932, _1935, _1936, _1937,
    _1940, _1942, _1944, _1946,
    _1948
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.mbd_analyses import _5099
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'GearMeshMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshMultiBodyDynamicsAnalysis',)


class GearMeshMultiBodyDynamicsAnalysis(_5099.InterMountableComponentConnectionMultiBodyDynamicsAnalysis):
    '''GearMeshMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def normal_stiffness(self) -> 'float':
        '''float: 'NormalStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalStiffness

    @property
    def normal_stiffness_left_flank(self) -> 'float':
        '''float: 'NormalStiffnessLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalStiffnessLeftFlank

    @property
    def normal_stiffness_right_flank(self) -> 'float':
        '''float: 'NormalStiffnessRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NormalStiffnessRightFlank

    @property
    def transverse_stiffness_left_flank(self) -> 'float':
        '''float: 'TransverseStiffnessLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseStiffnessLeftFlank

    @property
    def transverse_stiffness_right_flank(self) -> 'float':
        '''float: 'TransverseStiffnessRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseStiffnessRightFlank

    @property
    def tilt_stiffness(self) -> 'float':
        '''float: 'TiltStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TiltStiffness

    @property
    def contact_status(self) -> '_1394.GearMeshContactStatus':
        '''GearMeshContactStatus: 'ContactStatus' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_enum(self.wrapped.ContactStatus)
        return constructor.new(_1394.GearMeshContactStatus)(value) if value else None

    @property
    def separation(self) -> 'float':
        '''float: 'Separation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.Separation

    @property
    def separation_normal_to_left_flank(self) -> 'float':
        '''float: 'SeparationNormalToLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationNormalToLeftFlank

    @property
    def separation_normal_to_right_flank(self) -> 'float':
        '''float: 'SeparationNormalToRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationNormalToRightFlank

    @property
    def separation_transverse_to_left_flank(self) -> 'float':
        '''float: 'SeparationTransverseToLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationTransverseToLeftFlank

    @property
    def separation_transverse_to_right_flank(self) -> 'float':
        '''float: 'SeparationTransverseToRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SeparationTransverseToRightFlank

    @property
    def force_normal_to_left_flank(self) -> 'float':
        '''float: 'ForceNormalToLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceNormalToLeftFlank

    @property
    def force_normal_to_right_flank(self) -> 'float':
        '''float: 'ForceNormalToRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceNormalToRightFlank

    @property
    def average_sliding_velocity_left_flank(self) -> 'float':
        '''float: 'AverageSlidingVelocityLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageSlidingVelocityLeftFlank

    @property
    def average_sliding_velocity_right_flank(self) -> 'float':
        '''float: 'AverageSlidingVelocityRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AverageSlidingVelocityRightFlank

    @property
    def pitch_line_velocity_left_flank(self) -> 'float':
        '''float: 'PitchLineVelocityLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchLineVelocityLeftFlank

    @property
    def pitch_line_velocity_right_flank(self) -> 'float':
        '''float: 'PitchLineVelocityRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PitchLineVelocityRightFlank

    @property
    def misalignment_due_to_tilt_right_flank(self) -> 'float':
        '''float: 'MisalignmentDueToTiltRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MisalignmentDueToTiltRightFlank

    @property
    def misalignment_due_to_tilt_left_flank(self) -> 'float':
        '''float: 'MisalignmentDueToTiltLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MisalignmentDueToTiltLeftFlank

    @property
    def equivalent_misalignment_left_flank(self) -> 'float':
        '''float: 'EquivalentMisalignmentLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquivalentMisalignmentLeftFlank

    @property
    def equivalent_misalignment_right_flank(self) -> 'float':
        '''float: 'EquivalentMisalignmentRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.EquivalentMisalignmentRightFlank

    @property
    def mesh_power_loss(self) -> 'float':
        '''float: 'MeshPowerLoss' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MeshPowerLoss

    @property
    def coefficient_of_friction_left_flank(self) -> 'float':
        '''float: 'CoefficientOfFrictionLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientOfFrictionLeftFlank

    @property
    def coefficient_of_friction_right_flank(self) -> 'float':
        '''float: 'CoefficientOfFrictionRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CoefficientOfFrictionRightFlank

    @property
    def tooth_passing_frequency(self) -> 'float':
        '''float: 'ToothPassingFrequency' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothPassingFrequency

    @property
    def tooth_passing_speed_gear_a(self) -> 'float':
        '''float: 'ToothPassingSpeedGearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothPassingSpeedGearA

    @property
    def tooth_passing_speed_gear_b(self) -> 'float':
        '''float: 'ToothPassingSpeedGearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ToothPassingSpeedGearB

    @property
    def strain_energy_left_flank(self) -> 'float':
        '''float: 'StrainEnergyLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StrainEnergyLeftFlank

    @property
    def strain_energy_right_flank(self) -> 'float':
        '''float: 'StrainEnergyRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StrainEnergyRightFlank

    @property
    def strain_energy_total(self) -> 'float':
        '''float: 'StrainEnergyTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.StrainEnergyTotal

    @property
    def impact_power_left_flank(self) -> 'float':
        '''float: 'ImpactPowerLeftFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImpactPowerLeftFlank

    @property
    def impact_power_right_flank(self) -> 'float':
        '''float: 'ImpactPowerRightFlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImpactPowerRightFlank

    @property
    def impact_power_total(self) -> 'float':
        '''float: 'ImpactPowerTotal' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ImpactPowerTotal

    @property
    def connection_design(self) -> '_1930.GearMesh':
        '''GearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1930.GearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to GearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1916.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1916.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1918.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1918.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1920.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1922.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.ConceptGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_conical_gear_mesh(self) -> '_1924.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1924.ConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1926.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.CylindricalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1928.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1928.FaceGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1932.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1932.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1935.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1935.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1936.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1936.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1937.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1937.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1940.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1940.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1942.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1942.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1944.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1944.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_1946.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1946.WormGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1948.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1948.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

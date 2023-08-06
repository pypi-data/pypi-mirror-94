'''_3698.py

ConnectionPowerFlow
'''


from mastapy._internal import constructor
from mastapy.system_model.connections_and_sockets import (
    _1926, _1920, _1922, _1923,
    _1927, _1937, _1940, _1945,
    _1949
)
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.connections_and_sockets.gears import (
    _1953, _1955, _1957, _1959,
    _1961, _1963, _1965, _1967,
    _1969, _1972, _1973, _1974,
    _1977, _1979, _1981, _1983,
    _1985
)
from mastapy.system_model.connections_and_sockets.cycloidal import _1987, _1990, _1993
from mastapy.system_model.connections_and_sockets.couplings import (
    _1994, _1996, _1998, _2000,
    _2002, _2004
)
from mastapy.system_model.analyses_and_results.power_flows import _3751
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2362, _2328, _2329, _2334,
    _2336, _2341, _2346, _2349,
    _2352, _2355, _2359, _2364,
    _2367, _2371, _2372, _2374,
    _2375, _2376, _2387, _2392,
    _2396, _2400, _2401, _2404,
    _2407, _2419, _2422, _2428,
    _2431, _2438, _2440, _2443,
    _2446, _2449, _2461, _2469,
    _2472
)
from mastapy.system_model.analyses_and_results.analysis_cases import _7138
from mastapy._internal.python_net import python_net_import

_CONNECTION_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'ConnectionPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionPowerFlow',)


class ConnectionPowerFlow(_7138.ConnectionStaticLoadAnalysisCase):
    '''ConnectionPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def is_loaded(self) -> 'bool':
        '''bool: 'IsLoaded' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.IsLoaded

    @property
    def component_design(self) -> '_1926.Connection':
        '''Connection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.Connection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Connection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1920.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_belt_connection(self) -> '_1922.BeltConnection':
        '''BeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.BeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coaxial_connection(self) -> '_1923.CoaxialConnection':
        '''CoaxialConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1923.CoaxialConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cvt_belt_connection(self) -> '_1927.CVTBeltConnection':
        '''CVTBeltConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1927.CVTBeltConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_inter_mountable_component_connection(self) -> '_1937.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1937.InterMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_planetary_connection(self) -> '_1940.PlanetaryConnection':
        '''PlanetaryConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1940.PlanetaryConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_rolling_ring_connection(self) -> '_1945.RollingRingConnection':
        '''RollingRingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.RollingRingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft_to_mountable_component_connection(self) -> '_1949.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.ShaftToMountableComponentConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1953.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_differential_gear_mesh(self) -> '_1955.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1955.BevelDifferentialGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_bevel_gear_mesh(self) -> '_1957.BevelGearMesh':
        '''BevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.BevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_gear_mesh(self) -> '_1959.ConceptGearMesh':
        '''ConceptGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.ConceptGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_conical_gear_mesh(self) -> '_1961.ConicalGearMesh':
        '''ConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.ConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cylindrical_gear_mesh(self) -> '_1963.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.CylindricalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_face_gear_mesh(self) -> '_1965.FaceGearMesh':
        '''FaceGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.FaceGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_gear_mesh(self) -> '_1967.GearMesh':
        '''GearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1967.GearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to GearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_hypoid_gear_mesh(self) -> '_1969.HypoidGearMesh':
        '''HypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.HypoidGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1972.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1972.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1973.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1974.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spiral_bevel_gear_mesh(self) -> '_1977.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1977.SpiralBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1979.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_straight_bevel_gear_mesh(self) -> '_1981.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.StraightBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_worm_gear_mesh(self) -> '_1983.WormGearMesh':
        '''WormGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.WormGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_zerol_bevel_gear_mesh(self) -> '_1985.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.ZerolBevelGearMesh.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc_central_bearing_connection(self) -> '_1987.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_ring_pins_to_disc_connection(self) -> '_1993.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.RingPinsToDiscConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_clutch_connection(self) -> '_1994.ClutchConnection':
        '''ClutchConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.ClutchConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_concept_coupling_connection(self) -> '_1996.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.ConceptCouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_coupling_connection(self) -> '_1998.CouplingConnection':
        '''CouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.CouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_part_to_part_shear_coupling_connection(self) -> '_2000.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_spring_damper_connection(self) -> '_2002.SpringDamperConnection':
        '''SpringDamperConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.SpringDamperConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_torque_converter_connection(self) -> '_2004.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.TorqueConverterConnection.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def connection_design(self) -> '_1926.Connection':
        '''Connection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1926.Connection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to Connection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_abstract_shaft_to_mountable_component_connection(self) -> '_1920.AbstractShaftToMountableComponentConnection':
        '''AbstractShaftToMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1920.AbstractShaftToMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AbstractShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_belt_connection(self) -> '_1922.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1922.BeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coaxial_connection(self) -> '_1923.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1923.CoaxialConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CoaxialConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cvt_belt_connection(self) -> '_1927.CVTBeltConnection':
        '''CVTBeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1927.CVTBeltConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CVTBeltConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_inter_mountable_component_connection(self) -> '_1937.InterMountableComponentConnection':
        '''InterMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1937.InterMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to InterMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_planetary_connection(self) -> '_1940.PlanetaryConnection':
        '''PlanetaryConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1940.PlanetaryConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PlanetaryConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_rolling_ring_connection(self) -> '_1945.RollingRingConnection':
        '''RollingRingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1945.RollingRingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RollingRingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_shaft_to_mountable_component_connection(self) -> '_1949.ShaftToMountableComponentConnection':
        '''ShaftToMountableComponentConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1949.ShaftToMountableComponentConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ShaftToMountableComponentConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_agma_gleason_conical_gear_mesh(self) -> '_1953.AGMAGleasonConicalGearMesh':
        '''AGMAGleasonConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1953.AGMAGleasonConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to AGMAGleasonConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_differential_gear_mesh(self) -> '_1955.BevelDifferentialGearMesh':
        '''BevelDifferentialGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1955.BevelDifferentialGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelDifferentialGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_bevel_gear_mesh(self) -> '_1957.BevelGearMesh':
        '''BevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1957.BevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to BevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_gear_mesh(self) -> '_1959.ConceptGearMesh':
        '''ConceptGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1959.ConceptGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_conical_gear_mesh(self) -> '_1961.ConicalGearMesh':
        '''ConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1961.ConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cylindrical_gear_mesh(self) -> '_1963.CylindricalGearMesh':
        '''CylindricalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1963.CylindricalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CylindricalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_face_gear_mesh(self) -> '_1965.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1965.FaceGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to FaceGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_gear_mesh(self) -> '_1967.GearMesh':
        '''GearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1967.GearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to GearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_hypoid_gear_mesh(self) -> '_1969.HypoidGearMesh':
        '''HypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1969.HypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to HypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh(self) -> '_1972.KlingelnbergCycloPalloidConicalGearMesh':
        '''KlingelnbergCycloPalloidConicalGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1972.KlingelnbergCycloPalloidConicalGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidConicalGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self) -> '_1973.KlingelnbergCycloPalloidHypoidGearMesh':
        '''KlingelnbergCycloPalloidHypoidGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1973.KlingelnbergCycloPalloidHypoidGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidHypoidGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self) -> '_1974.KlingelnbergCycloPalloidSpiralBevelGearMesh':
        '''KlingelnbergCycloPalloidSpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1974.KlingelnbergCycloPalloidSpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to KlingelnbergCycloPalloidSpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spiral_bevel_gear_mesh(self) -> '_1977.SpiralBevelGearMesh':
        '''SpiralBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1977.SpiralBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpiralBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_diff_gear_mesh(self) -> '_1979.StraightBevelDiffGearMesh':
        '''StraightBevelDiffGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1979.StraightBevelDiffGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelDiffGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_straight_bevel_gear_mesh(self) -> '_1981.StraightBevelGearMesh':
        '''StraightBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1981.StraightBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to StraightBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_worm_gear_mesh(self) -> '_1983.WormGearMesh':
        '''WormGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1983.WormGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to WormGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_zerol_bevel_gear_mesh(self) -> '_1985.ZerolBevelGearMesh':
        '''ZerolBevelGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1985.ZerolBevelGearMesh.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ZerolBevelGearMesh. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cycloidal_disc_central_bearing_connection(self) -> '_1987.CycloidalDiscCentralBearingConnection':
        '''CycloidalDiscCentralBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1987.CycloidalDiscCentralBearingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CycloidalDiscCentralBearingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_cycloidal_disc_planetary_bearing_connection(self) -> '_1990.CycloidalDiscPlanetaryBearingConnection':
        '''CycloidalDiscPlanetaryBearingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1990.CycloidalDiscPlanetaryBearingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CycloidalDiscPlanetaryBearingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_ring_pins_to_disc_connection(self) -> '_1993.RingPinsToDiscConnection':
        '''RingPinsToDiscConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1993.RingPinsToDiscConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to RingPinsToDiscConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_clutch_connection(self) -> '_1994.ClutchConnection':
        '''ClutchConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1994.ClutchConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ClutchConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_concept_coupling_connection(self) -> '_1996.ConceptCouplingConnection':
        '''ConceptCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1996.ConceptCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to ConceptCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_coupling_connection(self) -> '_1998.CouplingConnection':
        '''CouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.CouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to CouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_part_to_part_shear_coupling_connection(self) -> '_2000.PartToPartShearCouplingConnection':
        '''PartToPartShearCouplingConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2000.PartToPartShearCouplingConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to PartToPartShearCouplingConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_spring_damper_connection(self) -> '_2002.SpringDamperConnection':
        '''SpringDamperConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2002.SpringDamperConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to SpringDamperConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_design_of_type_torque_converter_connection(self) -> '_2004.TorqueConverterConnection':
        '''TorqueConverterConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2004.TorqueConverterConnection.TYPE not in self.wrapped.ConnectionDesign.__class__.__mro__:
            raise CastException('Failed to cast connection_design to TorqueConverterConnection. Expected: {}.'.format(self.wrapped.ConnectionDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ConnectionDesign.__class__)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def power_flow(self) -> '_3751.PowerFlow':
        '''PowerFlow: 'PowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3751.PowerFlow)(self.wrapped.PowerFlow) if self.wrapped.PowerFlow else None

    @property
    def torsional_system_deflection_analysis(self) -> '_2362.ConnectionSystemDeflection':
        '''ConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2362.ConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_abstract_shaft_to_mountable_component_connection_system_deflection(self) -> '_2328.AbstractShaftToMountableComponentConnectionSystemDeflection':
        '''AbstractShaftToMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2328.AbstractShaftToMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to AbstractShaftToMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_agma_gleason_conical_gear_mesh_system_deflection(self) -> '_2329.AGMAGleasonConicalGearMeshSystemDeflection':
        '''AGMAGleasonConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2329.AGMAGleasonConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to AGMAGleasonConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_belt_connection_system_deflection(self) -> '_2334.BeltConnectionSystemDeflection':
        '''BeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2334.BeltConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_differential_gear_mesh_system_deflection(self) -> '_2336.BevelDifferentialGearMeshSystemDeflection':
        '''BevelDifferentialGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2336.BevelDifferentialGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelDifferentialGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_bevel_gear_mesh_system_deflection(self) -> '_2341.BevelGearMeshSystemDeflection':
        '''BevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2341.BevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to BevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_clutch_connection_system_deflection(self) -> '_2346.ClutchConnectionSystemDeflection':
        '''ClutchConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2346.ClutchConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ClutchConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coaxial_connection_system_deflection(self) -> '_2349.CoaxialConnectionSystemDeflection':
        '''CoaxialConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2349.CoaxialConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CoaxialConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_coupling_connection_system_deflection(self) -> '_2352.ConceptCouplingConnectionSystemDeflection':
        '''ConceptCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2352.ConceptCouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_concept_gear_mesh_system_deflection(self) -> '_2355.ConceptGearMeshSystemDeflection':
        '''ConceptGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2355.ConceptGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConceptGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_conical_gear_mesh_system_deflection(self) -> '_2359.ConicalGearMeshSystemDeflection':
        '''ConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2359.ConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_coupling_connection_system_deflection(self) -> '_2364.CouplingConnectionSystemDeflection':
        '''CouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2364.CouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cvt_belt_connection_system_deflection(self) -> '_2367.CVTBeltConnectionSystemDeflection':
        '''CVTBeltConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2367.CVTBeltConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CVTBeltConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cycloidal_disc_central_bearing_connection_system_deflection(self) -> '_2371.CycloidalDiscCentralBearingConnectionSystemDeflection':
        '''CycloidalDiscCentralBearingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2371.CycloidalDiscCentralBearingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CycloidalDiscCentralBearingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cycloidal_disc_planetary_bearing_connection_system_deflection(self) -> '_2372.CycloidalDiscPlanetaryBearingConnectionSystemDeflection':
        '''CycloidalDiscPlanetaryBearingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2372.CycloidalDiscPlanetaryBearingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CycloidalDiscPlanetaryBearingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection(self) -> '_2374.CylindricalGearMeshSystemDeflection':
        '''CylindricalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2374.CylindricalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_timestep(self) -> '_2375.CylindricalGearMeshSystemDeflectionTimestep':
        '''CylindricalGearMeshSystemDeflectionTimestep: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2375.CylindricalGearMeshSystemDeflectionTimestep.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionTimestep. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_cylindrical_gear_mesh_system_deflection_with_ltca_results(self) -> '_2376.CylindricalGearMeshSystemDeflectionWithLTCAResults':
        '''CylindricalGearMeshSystemDeflectionWithLTCAResults: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2376.CylindricalGearMeshSystemDeflectionWithLTCAResults.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to CylindricalGearMeshSystemDeflectionWithLTCAResults. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_face_gear_mesh_system_deflection(self) -> '_2387.FaceGearMeshSystemDeflection':
        '''FaceGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2387.FaceGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to FaceGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_gear_mesh_system_deflection(self) -> '_2392.GearMeshSystemDeflection':
        '''GearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2392.GearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to GearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_hypoid_gear_mesh_system_deflection(self) -> '_2396.HypoidGearMeshSystemDeflection':
        '''HypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2396.HypoidGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to HypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_inter_mountable_component_connection_system_deflection(self) -> '_2400.InterMountableComponentConnectionSystemDeflection':
        '''InterMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2400.InterMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to InterMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_conical_gear_mesh_system_deflection(self) -> '_2401.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidConicalGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2401.KlingelnbergCycloPalloidConicalGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidConicalGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_hypoid_gear_mesh_system_deflection(self) -> '_2404.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2404.KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidHypoidGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_system_deflection(self) -> '_2407.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection':
        '''KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2407.KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to KlingelnbergCycloPalloidSpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_part_to_part_shear_coupling_connection_system_deflection(self) -> '_2419.PartToPartShearCouplingConnectionSystemDeflection':
        '''PartToPartShearCouplingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2419.PartToPartShearCouplingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to PartToPartShearCouplingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_planetary_connection_system_deflection(self) -> '_2422.PlanetaryConnectionSystemDeflection':
        '''PlanetaryConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2422.PlanetaryConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to PlanetaryConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_ring_pins_to_disc_connection_system_deflection(self) -> '_2428.RingPinsToDiscConnectionSystemDeflection':
        '''RingPinsToDiscConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2428.RingPinsToDiscConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to RingPinsToDiscConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_rolling_ring_connection_system_deflection(self) -> '_2431.RollingRingConnectionSystemDeflection':
        '''RollingRingConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2431.RollingRingConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to RollingRingConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_shaft_to_mountable_component_connection_system_deflection(self) -> '_2438.ShaftToMountableComponentConnectionSystemDeflection':
        '''ShaftToMountableComponentConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2438.ShaftToMountableComponentConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ShaftToMountableComponentConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spiral_bevel_gear_mesh_system_deflection(self) -> '_2440.SpiralBevelGearMeshSystemDeflection':
        '''SpiralBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2440.SpiralBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpiralBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_spring_damper_connection_system_deflection(self) -> '_2443.SpringDamperConnectionSystemDeflection':
        '''SpringDamperConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2443.SpringDamperConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to SpringDamperConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_diff_gear_mesh_system_deflection(self) -> '_2446.StraightBevelDiffGearMeshSystemDeflection':
        '''StraightBevelDiffGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2446.StraightBevelDiffGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelDiffGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_straight_bevel_gear_mesh_system_deflection(self) -> '_2449.StraightBevelGearMeshSystemDeflection':
        '''StraightBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2449.StraightBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to StraightBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_torque_converter_connection_system_deflection(self) -> '_2461.TorqueConverterConnectionSystemDeflection':
        '''TorqueConverterConnectionSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2461.TorqueConverterConnectionSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to TorqueConverterConnectionSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_worm_gear_mesh_system_deflection(self) -> '_2469.WormGearMeshSystemDeflection':
        '''WormGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2469.WormGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to WormGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

    @property
    def torsional_system_deflection_analysis_of_type_zerol_bevel_gear_mesh_system_deflection(self) -> '_2472.ZerolBevelGearMeshSystemDeflection':
        '''ZerolBevelGearMeshSystemDeflection: 'TorsionalSystemDeflectionAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2472.ZerolBevelGearMeshSystemDeflection.TYPE not in self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__mro__:
            raise CastException('Failed to cast torsional_system_deflection_analysis to ZerolBevelGearMeshSystemDeflection. Expected: {}.'.format(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__.__qualname__))

        return constructor.new_override(self.wrapped.TorsionalSystemDeflectionAnalysis.__class__)(self.wrapped.TorsionalSystemDeflectionAnalysis) if self.wrapped.TorsionalSystemDeflectionAnalysis else None

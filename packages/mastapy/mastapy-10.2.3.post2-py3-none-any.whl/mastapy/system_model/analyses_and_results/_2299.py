'''_2299.py

CompoundAdvancedSystemDeflectionAnalysis
'''


from typing import Iterable

from mastapy.system_model.connections_and_sockets.couplings import (
    _2002, _2004, _2000, _1994,
    _1996, _1998
)
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _7106, _7121, _7004, _7003,
    _7005, _7011, _7022, _7023,
    _7028, _7039, _7054, _7055,
    _7059, _7060, _7010, _7064,
    _7078, _7079, _7080, _7081,
    _7082, _7088, _7089, _7090,
    _7097, _7101, _7124, _7125,
    _7098, _7032, _7034, _7056,
    _7058, _7007, _7009, _7014,
    _7016, _7017, _7018, _7019,
    _7021, _7035, _7037, _7050,
    _7052, _7053, _7061, _7063,
    _7065, _7067, _7069, _7071,
    _7072, _7074, _7075, _7077,
    _7087, _7102, _7104, _7108,
    _7110, _7111, _7113, _7114,
    _7115, _7126, _7128, _7129,
    _7131, _7046, _7048, _7092,
    _7083, _7085, _7013, _7024,
    _7026, _7029, _7031, _7040,
    _7042, _7044, _7045, _7091,
    _7099, _7095, _7094, _7105,
    _7107, _7116, _7117, _7118,
    _7119, _7120, _7122, _7123,
    _7100, _7043, _7012, _7027,
    _7038, _7068, _7086, _7096,
    _7006, _7015, _7033, _7057,
    _7109, _7020, _7036, _7008,
    _7051, _7066, _7070, _7073,
    _7076, _7103, _7112, _7127,
    _7130, _7062, _7047, _7049,
    _7093, _7084, _7025, _7030,
    _7041
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import (
    _2085, _2084, _2086, _2089,
    _2091, _2092, _2093, _2096,
    _2097, _2100, _2101, _2102,
    _2083, _2103, _2110, _2111,
    _2112, _2114, _2116, _2117,
    _2119, _2120, _2122, _2124,
    _2125, _2126
)
from mastapy.system_model.part_model.shaft_model import _2129
from mastapy.system_model.part_model.gears import (
    _2167, _2168, _2174, _2175,
    _2159, _2160, _2161, _2162,
    _2163, _2164, _2165, _2166,
    _2169, _2170, _2171, _2172,
    _2173, _2176, _2178, _2180,
    _2181, _2182, _2183, _2184,
    _2185, _2186, _2187, _2188,
    _2189, _2190, _2191, _2192,
    _2193, _2194, _2195, _2196,
    _2197, _2198, _2199, _2200
)
from mastapy.system_model.part_model.cycloidal import _2214, _2215, _2216
from mastapy.system_model.part_model.couplings import (
    _2234, _2235, _2222, _2224,
    _2225, _2227, _2228, _2229,
    _2230, _2232, _2233, _2236,
    _2244, _2242, _2243, _2245,
    _2246, _2247, _2249, _2250,
    _2251, _2252, _2253, _2255
)
from mastapy.system_model.connections_and_sockets import (
    _1949, _1927, _1922, _1923,
    _1926, _1937, _1940, _1945,
    _1920
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1955, _1959, _1965, _1979,
    _1957, _1961, _1953, _1963,
    _1969, _1972, _1973, _1974,
    _1977, _1981, _1983, _1985,
    _1967
)
from mastapy.system_model.connections_and_sockets.cycloidal import _1987, _1990, _1993
from mastapy._internal.python_net import python_net_import
from mastapy.system_model.analyses_and_results import _2264

_SPRING_DAMPER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'SpringDamperConnection')
_TORQUE_CONVERTER_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'TorqueConverterConnection')
_PART_TO_PART_SHEAR_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'PartToPartShearCouplingConnection')
_CLUTCH_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ClutchConnection')
_CONCEPT_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'ConceptCouplingConnection')
_COUPLING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Couplings', 'CouplingConnection')
_ABSTRACT_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaft')
_ABSTRACT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractAssembly')
_ABSTRACT_SHAFT_OR_HOUSING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'AbstractShaftOrHousing')
_BEARING = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bearing')
_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')
_BOLTED_JOINT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'BoltedJoint')
_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Component')
_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')
_DATUM = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Datum')
_EXTERNAL_CAD_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'ExternalCADModel')
_FE_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FEPart')
_FLEXIBLE_PIN_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'FlexiblePinAssembly')
_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Assembly')
_GUIDE_DXF_MODEL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'GuideDxfModel')
_MASS_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MassDisc')
_MEASUREMENT_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MeasurementComponent')
_MOUNTABLE_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'MountableComponent')
_OIL_SEAL = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'OilSeal')
_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Part')
_PLANET_CARRIER = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PlanetCarrier')
_POINT_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PointLoad')
_POWER_LOAD = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'PowerLoad')
_ROOT_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'RootAssembly')
_SPECIALISED_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'SpecialisedAssembly')
_UNBALANCED_MASS = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'UnbalancedMass')
_VIRTUAL_COMPONENT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'VirtualComponent')
_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.ShaftModel', 'Shaft')
_CONCEPT_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGear')
_CONCEPT_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConceptGearSet')
_FACE_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGear')
_FACE_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'FaceGearSet')
_AGMA_GLEASON_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGear')
_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'AGMAGleasonConicalGearSet')
_BEVEL_DIFFERENTIAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGear')
_BEVEL_DIFFERENTIAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialGearSet')
_BEVEL_DIFFERENTIAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialPlanetGear')
_BEVEL_DIFFERENTIAL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelDifferentialSunGear')
_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')
_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGearSet')
_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGear')
_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ConicalGearSet')
_CYLINDRICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGear')
_CYLINDRICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalGearSet')
_CYLINDRICAL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'CylindricalPlanetGear')
_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'Gear')
_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'GearSet')
_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGear')
_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'HypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGear')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidConicalGearSet')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGear')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidHypoidGearSet')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGear')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearSet')
_PLANETARY_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'PlanetaryGearSet')
_SPIRAL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGear')
_SPIRAL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'SpiralBevelGearSet')
_STRAIGHT_BEVEL_DIFF_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGear')
_STRAIGHT_BEVEL_DIFF_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelDiffGearSet')
_STRAIGHT_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGear')
_STRAIGHT_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelGearSet')
_STRAIGHT_BEVEL_PLANET_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelPlanetGear')
_STRAIGHT_BEVEL_SUN_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'StraightBevelSunGear')
_WORM_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGear')
_WORM_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'WormGearSet')
_ZEROL_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGear')
_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')
_CYCLOIDAL_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalAssembly')
_CYCLOIDAL_DISC = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'CycloidalDisc')
_RING_PINS = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Cycloidal', 'RingPins')
_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')
_PART_TO_PART_SHEAR_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCouplingHalf')
_BELT_DRIVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'BeltDrive')
_CLUTCH = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Clutch')
_CLUTCH_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ClutchHalf')
_CONCEPT_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCoupling')
_CONCEPT_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ConceptCouplingHalf')
_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Coupling')
_COUPLING_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CouplingHalf')
_CVT = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVT')
_CVT_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'CVTPulley')
_PULLEY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Pulley')
_SHAFT_HUB_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'ShaftHubConnection')
_ROLLING_RING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRing')
_ROLLING_RING_ASSEMBLY = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'RollingRingAssembly')
_SPRING_DAMPER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamper')
_SPRING_DAMPER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SpringDamperHalf')
_SYNCHRONISER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'Synchroniser')
_SYNCHRONISER_HALF = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserHalf')
_SYNCHRONISER_PART = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserPart')
_SYNCHRONISER_SLEEVE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'SynchroniserSleeve')
_TORQUE_CONVERTER = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverter')
_TORQUE_CONVERTER_PUMP = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterPump')
_TORQUE_CONVERTER_TURBINE = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'TorqueConverterTurbine')
_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'ShaftToMountableComponentConnection')
_CVT_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTBeltConnection')
_BELT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'BeltConnection')
_COAXIAL_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CoaxialConnection')
_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'Connection')
_INTER_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'InterMountableComponentConnection')
_PLANETARY_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'PlanetaryConnection')
_ROLLING_RING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'RollingRingConnection')
_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'AbstractShaftToMountableComponentConnection')
_BEVEL_DIFFERENTIAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelDifferentialGearMesh')
_CONCEPT_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConceptGearMesh')
_FACE_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'FaceGearMesh')
_STRAIGHT_BEVEL_DIFF_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelDiffGearMesh')
_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'BevelGearMesh')
_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ConicalGearMesh')
_AGMA_GLEASON_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'AGMAGleasonConicalGearMesh')
_CYLINDRICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'CylindricalGearMesh')
_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'HypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidConicalGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidHypoidGearMesh')
_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'KlingelnbergCycloPalloidSpiralBevelGearMesh')
_SPIRAL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'SpiralBevelGearMesh')
_STRAIGHT_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'StraightBevelGearMesh')
_WORM_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'WormGearMesh')
_ZEROL_BEVEL_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'ZerolBevelGearMesh')
_GEAR_MESH = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Gears', 'GearMesh')
_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscCentralBearingConnection')
_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'CycloidalDiscPlanetaryBearingConnection')
_RING_PINS_TO_DISC_CONNECTION = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets.Cycloidal', 'RingPinsToDiscConnection')
_COMPOUND_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundAdvancedSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundAdvancedSystemDeflectionAnalysis',)


class CompoundAdvancedSystemDeflectionAnalysis(_2264.CompoundAnalysis):
    '''CompoundAdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundAdvancedSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    def results_for_spring_damper_connection(self, design_entity: '_2002.SpringDamperConnection') -> 'Iterable[_7106.SpringDamperConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7106.SpringDamperConnectionCompoundAdvancedSystemDeflection))

    def results_for_torque_converter_connection(self, design_entity: '_2004.TorqueConverterConnection') -> 'Iterable[_7121.TorqueConverterConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7121.TorqueConverterConnectionCompoundAdvancedSystemDeflection))

    def results_for_abstract_shaft(self, design_entity: '_2085.AbstractShaft') -> 'Iterable[_7004.AbstractShaftCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_7004.AbstractShaftCompoundAdvancedSystemDeflection))

    def results_for_abstract_assembly(self, design_entity: '_2084.AbstractAssembly') -> 'Iterable[_7003.AbstractAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7003.AbstractAssemblyCompoundAdvancedSystemDeflection))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_2086.AbstractShaftOrHousing') -> 'Iterable[_7005.AbstractShaftOrHousingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftOrHousingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_OR_HOUSING](design_entity.wrapped if design_entity else None), constructor.new(_7005.AbstractShaftOrHousingCompoundAdvancedSystemDeflection))

    def results_for_bearing(self, design_entity: '_2089.Bearing') -> 'Iterable[_7011.BearingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BearingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEARING](design_entity.wrapped if design_entity else None), constructor.new(_7011.BearingCompoundAdvancedSystemDeflection))

    def results_for_bolt(self, design_entity: '_2091.Bolt') -> 'Iterable[_7022.BoltCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BoltCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLT](design_entity.wrapped if design_entity else None), constructor.new(_7022.BoltCompoundAdvancedSystemDeflection))

    def results_for_bolted_joint(self, design_entity: '_2092.BoltedJoint') -> 'Iterable[_7023.BoltedJointCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BoltedJointCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BOLTED_JOINT](design_entity.wrapped if design_entity else None), constructor.new(_7023.BoltedJointCompoundAdvancedSystemDeflection))

    def results_for_component(self, design_entity: '_2093.Component') -> 'Iterable[_7028.ComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_7028.ComponentCompoundAdvancedSystemDeflection))

    def results_for_connector(self, design_entity: '_2096.Connector') -> 'Iterable[_7039.ConnectorCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConnectorCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTOR](design_entity.wrapped if design_entity else None), constructor.new(_7039.ConnectorCompoundAdvancedSystemDeflection))

    def results_for_datum(self, design_entity: '_2097.Datum') -> 'Iterable[_7054.DatumCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.DatumCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_DATUM](design_entity.wrapped if design_entity else None), constructor.new(_7054.DatumCompoundAdvancedSystemDeflection))

    def results_for_external_cad_model(self, design_entity: '_2100.ExternalCADModel') -> 'Iterable[_7055.ExternalCADModelCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ExternalCADModelCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_EXTERNAL_CAD_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_7055.ExternalCADModelCompoundAdvancedSystemDeflection))

    def results_for_fe_part(self, design_entity: '_2101.FEPart') -> 'Iterable[_7059.FEPartCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FEPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FEPartCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FE_PART](design_entity.wrapped if design_entity else None), constructor.new(_7059.FEPartCompoundAdvancedSystemDeflection))

    def results_for_flexible_pin_assembly(self, design_entity: '_2102.FlexiblePinAssembly') -> 'Iterable[_7060.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FLEXIBLE_PIN_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7060.FlexiblePinAssemblyCompoundAdvancedSystemDeflection))

    def results_for_assembly(self, design_entity: '_2083.Assembly') -> 'Iterable[_7010.AssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7010.AssemblyCompoundAdvancedSystemDeflection))

    def results_for_guide_dxf_model(self, design_entity: '_2103.GuideDxfModel') -> 'Iterable[_7064.GuideDxfModelCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GuideDxfModelCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GUIDE_DXF_MODEL](design_entity.wrapped if design_entity else None), constructor.new(_7064.GuideDxfModelCompoundAdvancedSystemDeflection))

    def results_for_mass_disc(self, design_entity: '_2110.MassDisc') -> 'Iterable[_7078.MassDiscCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MassDiscCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MASS_DISC](design_entity.wrapped if design_entity else None), constructor.new(_7078.MassDiscCompoundAdvancedSystemDeflection))

    def results_for_measurement_component(self, design_entity: '_2111.MeasurementComponent') -> 'Iterable[_7079.MeasurementComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MeasurementComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MEASUREMENT_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_7079.MeasurementComponentCompoundAdvancedSystemDeflection))

    def results_for_mountable_component(self, design_entity: '_2112.MountableComponent') -> 'Iterable[_7080.MountableComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.MountableComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_MOUNTABLE_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_7080.MountableComponentCompoundAdvancedSystemDeflection))

    def results_for_oil_seal(self, design_entity: '_2114.OilSeal') -> 'Iterable[_7081.OilSealCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.OilSealCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_OIL_SEAL](design_entity.wrapped if design_entity else None), constructor.new(_7081.OilSealCompoundAdvancedSystemDeflection))

    def results_for_part(self, design_entity: '_2116.Part') -> 'Iterable[_7082.PartCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART](design_entity.wrapped if design_entity else None), constructor.new(_7082.PartCompoundAdvancedSystemDeflection))

    def results_for_planet_carrier(self, design_entity: '_2117.PlanetCarrier') -> 'Iterable[_7088.PlanetCarrierCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetCarrierCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANET_CARRIER](design_entity.wrapped if design_entity else None), constructor.new(_7088.PlanetCarrierCompoundAdvancedSystemDeflection))

    def results_for_point_load(self, design_entity: '_2119.PointLoad') -> 'Iterable[_7089.PointLoadCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PointLoadCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POINT_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_7089.PointLoadCompoundAdvancedSystemDeflection))

    def results_for_power_load(self, design_entity: '_2120.PowerLoad') -> 'Iterable[_7090.PowerLoadCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PowerLoadCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_POWER_LOAD](design_entity.wrapped if design_entity else None), constructor.new(_7090.PowerLoadCompoundAdvancedSystemDeflection))

    def results_for_root_assembly(self, design_entity: '_2122.RootAssembly') -> 'Iterable[_7097.RootAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RootAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROOT_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7097.RootAssemblyCompoundAdvancedSystemDeflection))

    def results_for_specialised_assembly(self, design_entity: '_2124.SpecialisedAssembly') -> 'Iterable[_7101.SpecialisedAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpecialisedAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPECIALISED_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7101.SpecialisedAssemblyCompoundAdvancedSystemDeflection))

    def results_for_unbalanced_mass(self, design_entity: '_2125.UnbalancedMass') -> 'Iterable[_7124.UnbalancedMassCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.UnbalancedMassCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_UNBALANCED_MASS](design_entity.wrapped if design_entity else None), constructor.new(_7124.UnbalancedMassCompoundAdvancedSystemDeflection))

    def results_for_virtual_component(self, design_entity: '_2126.VirtualComponent') -> 'Iterable[_7125.VirtualComponentCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.VirtualComponentCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_VIRTUAL_COMPONENT](design_entity.wrapped if design_entity else None), constructor.new(_7125.VirtualComponentCompoundAdvancedSystemDeflection))

    def results_for_shaft(self, design_entity: '_2129.Shaft') -> 'Iterable[_7098.ShaftCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT](design_entity.wrapped if design_entity else None), constructor.new(_7098.ShaftCompoundAdvancedSystemDeflection))

    def results_for_concept_gear(self, design_entity: '_2167.ConceptGear') -> 'Iterable[_7032.ConceptGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7032.ConceptGearCompoundAdvancedSystemDeflection))

    def results_for_concept_gear_set(self, design_entity: '_2168.ConceptGearSet') -> 'Iterable[_7034.ConceptGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7034.ConceptGearSetCompoundAdvancedSystemDeflection))

    def results_for_face_gear(self, design_entity: '_2174.FaceGear') -> 'Iterable[_7056.FaceGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7056.FaceGearCompoundAdvancedSystemDeflection))

    def results_for_face_gear_set(self, design_entity: '_2175.FaceGearSet') -> 'Iterable[_7058.FaceGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7058.FaceGearSetCompoundAdvancedSystemDeflection))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2159.AGMAGleasonConicalGear') -> 'Iterable[_7007.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7007.AGMAGleasonConicalGearCompoundAdvancedSystemDeflection))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2160.AGMAGleasonConicalGearSet') -> 'Iterable[_7009.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7009.AGMAGleasonConicalGearSetCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_gear(self, design_entity: '_2161.BevelDifferentialGear') -> 'Iterable[_7014.BevelDifferentialGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7014.BevelDifferentialGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2162.BevelDifferentialGearSet') -> 'Iterable[_7016.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7016.BevelDifferentialGearSetCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2163.BevelDifferentialPlanetGear') -> 'Iterable[_7017.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7017.BevelDifferentialPlanetGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2164.BevelDifferentialSunGear') -> 'Iterable[_7018.BevelDifferentialSunGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialSunGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7018.BevelDifferentialSunGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_gear(self, design_entity: '_2165.BevelGear') -> 'Iterable[_7019.BevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7019.BevelGearCompoundAdvancedSystemDeflection))

    def results_for_bevel_gear_set(self, design_entity: '_2166.BevelGearSet') -> 'Iterable[_7021.BevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7021.BevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_conical_gear(self, design_entity: '_2169.ConicalGear') -> 'Iterable[_7035.ConicalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7035.ConicalGearCompoundAdvancedSystemDeflection))

    def results_for_conical_gear_set(self, design_entity: '_2170.ConicalGearSet') -> 'Iterable[_7037.ConicalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7037.ConicalGearSetCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_gear(self, design_entity: '_2171.CylindricalGear') -> 'Iterable[_7050.CylindricalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7050.CylindricalGearCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_gear_set(self, design_entity: '_2172.CylindricalGearSet') -> 'Iterable[_7052.CylindricalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7052.CylindricalGearSetCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2173.CylindricalPlanetGear') -> 'Iterable[_7053.CylindricalPlanetGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalPlanetGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7053.CylindricalPlanetGearCompoundAdvancedSystemDeflection))

    def results_for_gear(self, design_entity: '_2176.Gear') -> 'Iterable[_7061.GearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7061.GearCompoundAdvancedSystemDeflection))

    def results_for_gear_set(self, design_entity: '_2178.GearSet') -> 'Iterable[_7063.GearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7063.GearSetCompoundAdvancedSystemDeflection))

    def results_for_hypoid_gear(self, design_entity: '_2180.HypoidGear') -> 'Iterable[_7065.HypoidGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7065.HypoidGearCompoundAdvancedSystemDeflection))

    def results_for_hypoid_gear_set(self, design_entity: '_2181.HypoidGearSet') -> 'Iterable[_7067.HypoidGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7067.HypoidGearSetCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2182.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_7069.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7069.KlingelnbergCycloPalloidConicalGearCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2183.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_7071.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7071.KlingelnbergCycloPalloidConicalGearSetCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2184.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_7072.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7072.KlingelnbergCycloPalloidHypoidGearCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2185.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_7074.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7074.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2186.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_7075.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7075.KlingelnbergCycloPalloidSpiralBevelGearCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2187.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_7077.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7077.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_planetary_gear_set(self, design_entity: '_2188.PlanetaryGearSet') -> 'Iterable[_7087.PlanetaryGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetaryGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7087.PlanetaryGearSetCompoundAdvancedSystemDeflection))

    def results_for_spiral_bevel_gear(self, design_entity: '_2189.SpiralBevelGear') -> 'Iterable[_7102.SpiralBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7102.SpiralBevelGearCompoundAdvancedSystemDeflection))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2190.SpiralBevelGearSet') -> 'Iterable[_7104.SpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7104.SpiralBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2191.StraightBevelDiffGear') -> 'Iterable[_7108.StraightBevelDiffGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7108.StraightBevelDiffGearCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2192.StraightBevelDiffGearSet') -> 'Iterable[_7110.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7110.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_gear(self, design_entity: '_2193.StraightBevelGear') -> 'Iterable[_7111.StraightBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7111.StraightBevelGearCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2194.StraightBevelGearSet') -> 'Iterable[_7113.StraightBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7113.StraightBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2195.StraightBevelPlanetGear') -> 'Iterable[_7114.StraightBevelPlanetGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelPlanetGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_PLANET_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7114.StraightBevelPlanetGearCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2196.StraightBevelSunGear') -> 'Iterable[_7115.StraightBevelSunGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelSunGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_SUN_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7115.StraightBevelSunGearCompoundAdvancedSystemDeflection))

    def results_for_worm_gear(self, design_entity: '_2197.WormGear') -> 'Iterable[_7126.WormGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7126.WormGearCompoundAdvancedSystemDeflection))

    def results_for_worm_gear_set(self, design_entity: '_2198.WormGearSet') -> 'Iterable[_7128.WormGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7128.WormGearSetCompoundAdvancedSystemDeflection))

    def results_for_zerol_bevel_gear(self, design_entity: '_2199.ZerolBevelGear') -> 'Iterable[_7129.ZerolBevelGearCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR](design_entity.wrapped if design_entity else None), constructor.new(_7129.ZerolBevelGearCompoundAdvancedSystemDeflection))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2200.ZerolBevelGearSet') -> 'Iterable[_7131.ZerolBevelGearSetCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearSetCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_SET](design_entity.wrapped if design_entity else None), constructor.new(_7131.ZerolBevelGearSetCompoundAdvancedSystemDeflection))

    def results_for_cycloidal_assembly(self, design_entity: '_2214.CycloidalAssembly') -> 'Iterable[_7046.CycloidalAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7046.CycloidalAssemblyCompoundAdvancedSystemDeflection))

    def results_for_cycloidal_disc(self, design_entity: '_2215.CycloidalDisc') -> 'Iterable[_7048.CycloidalDiscCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.CycloidalDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalDiscCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC](design_entity.wrapped if design_entity else None), constructor.new(_7048.CycloidalDiscCompoundAdvancedSystemDeflection))

    def results_for_ring_pins(self, design_entity: '_2216.RingPins') -> 'Iterable[_7092.RingPinsCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.cycloidal.RingPins)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RingPinsCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_RING_PINS](design_entity.wrapped if design_entity else None), constructor.new(_7092.RingPinsCompoundAdvancedSystemDeflection))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2234.PartToPartShearCoupling') -> 'Iterable[_7083.PartToPartShearCouplingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_7083.PartToPartShearCouplingCompoundAdvancedSystemDeflection))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2235.PartToPartShearCouplingHalf') -> 'Iterable[_7085.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_7085.PartToPartShearCouplingHalfCompoundAdvancedSystemDeflection))

    def results_for_belt_drive(self, design_entity: '_2222.BeltDrive') -> 'Iterable[_7013.BeltDriveCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BeltDriveCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_DRIVE](design_entity.wrapped if design_entity else None), constructor.new(_7013.BeltDriveCompoundAdvancedSystemDeflection))

    def results_for_clutch(self, design_entity: '_2224.Clutch') -> 'Iterable[_7024.ClutchCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH](design_entity.wrapped if design_entity else None), constructor.new(_7024.ClutchCompoundAdvancedSystemDeflection))

    def results_for_clutch_half(self, design_entity: '_2225.ClutchHalf') -> 'Iterable[_7026.ClutchHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_HALF](design_entity.wrapped if design_entity else None), constructor.new(_7026.ClutchHalfCompoundAdvancedSystemDeflection))

    def results_for_concept_coupling(self, design_entity: '_2227.ConceptCoupling') -> 'Iterable[_7029.ConceptCouplingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_7029.ConceptCouplingCompoundAdvancedSystemDeflection))

    def results_for_concept_coupling_half(self, design_entity: '_2228.ConceptCouplingHalf') -> 'Iterable[_7031.ConceptCouplingHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_7031.ConceptCouplingHalfCompoundAdvancedSystemDeflection))

    def results_for_coupling(self, design_entity: '_2229.Coupling') -> 'Iterable[_7040.CouplingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING](design_entity.wrapped if design_entity else None), constructor.new(_7040.CouplingCompoundAdvancedSystemDeflection))

    def results_for_coupling_half(self, design_entity: '_2230.CouplingHalf') -> 'Iterable[_7042.CouplingHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_HALF](design_entity.wrapped if design_entity else None), constructor.new(_7042.CouplingHalfCompoundAdvancedSystemDeflection))

    def results_for_cvt(self, design_entity: '_2232.CVT') -> 'Iterable[_7044.CVTCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT](design_entity.wrapped if design_entity else None), constructor.new(_7044.CVTCompoundAdvancedSystemDeflection))

    def results_for_cvt_pulley(self, design_entity: '_2233.CVTPulley') -> 'Iterable[_7045.CVTPulleyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTPulleyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_7045.CVTPulleyCompoundAdvancedSystemDeflection))

    def results_for_pulley(self, design_entity: '_2236.Pulley') -> 'Iterable[_7091.PulleyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PulleyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PULLEY](design_entity.wrapped if design_entity else None), constructor.new(_7091.PulleyCompoundAdvancedSystemDeflection))

    def results_for_shaft_hub_connection(self, design_entity: '_2244.ShaftHubConnection') -> 'Iterable[_7099.ShaftHubConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftHubConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_HUB_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7099.ShaftHubConnectionCompoundAdvancedSystemDeflection))

    def results_for_rolling_ring(self, design_entity: '_2242.RollingRing') -> 'Iterable[_7095.RollingRingCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING](design_entity.wrapped if design_entity else None), constructor.new(_7095.RollingRingCompoundAdvancedSystemDeflection))

    def results_for_rolling_ring_assembly(self, design_entity: '_2243.RollingRingAssembly') -> 'Iterable[_7094.RollingRingAssemblyCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingAssemblyCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_ASSEMBLY](design_entity.wrapped if design_entity else None), constructor.new(_7094.RollingRingAssemblyCompoundAdvancedSystemDeflection))

    def results_for_spring_damper(self, design_entity: '_2245.SpringDamper') -> 'Iterable[_7105.SpringDamperCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER](design_entity.wrapped if design_entity else None), constructor.new(_7105.SpringDamperCompoundAdvancedSystemDeflection))

    def results_for_spring_damper_half(self, design_entity: '_2246.SpringDamperHalf') -> 'Iterable[_7107.SpringDamperHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpringDamperHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPRING_DAMPER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_7107.SpringDamperHalfCompoundAdvancedSystemDeflection))

    def results_for_synchroniser(self, design_entity: '_2247.Synchroniser') -> 'Iterable[_7116.SynchroniserCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER](design_entity.wrapped if design_entity else None), constructor.new(_7116.SynchroniserCompoundAdvancedSystemDeflection))

    def results_for_synchroniser_half(self, design_entity: '_2249.SynchroniserHalf') -> 'Iterable[_7117.SynchroniserHalfCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserHalfCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_HALF](design_entity.wrapped if design_entity else None), constructor.new(_7117.SynchroniserHalfCompoundAdvancedSystemDeflection))

    def results_for_synchroniser_part(self, design_entity: '_2250.SynchroniserPart') -> 'Iterable[_7118.SynchroniserPartCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserPartCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_PART](design_entity.wrapped if design_entity else None), constructor.new(_7118.SynchroniserPartCompoundAdvancedSystemDeflection))

    def results_for_synchroniser_sleeve(self, design_entity: '_2251.SynchroniserSleeve') -> 'Iterable[_7119.SynchroniserSleeveCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SynchroniserSleeveCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SYNCHRONISER_SLEEVE](design_entity.wrapped if design_entity else None), constructor.new(_7119.SynchroniserSleeveCompoundAdvancedSystemDeflection))

    def results_for_torque_converter(self, design_entity: '_2252.TorqueConverter') -> 'Iterable[_7120.TorqueConverterCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER](design_entity.wrapped if design_entity else None), constructor.new(_7120.TorqueConverterCompoundAdvancedSystemDeflection))

    def results_for_torque_converter_pump(self, design_entity: '_2253.TorqueConverterPump') -> 'Iterable[_7122.TorqueConverterPumpCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterPumpCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_PUMP](design_entity.wrapped if design_entity else None), constructor.new(_7122.TorqueConverterPumpCompoundAdvancedSystemDeflection))

    def results_for_torque_converter_turbine(self, design_entity: '_2255.TorqueConverterTurbine') -> 'Iterable[_7123.TorqueConverterTurbineCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.TorqueConverterTurbineCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_TORQUE_CONVERTER_TURBINE](design_entity.wrapped if design_entity else None), constructor.new(_7123.TorqueConverterTurbineCompoundAdvancedSystemDeflection))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1949.ShaftToMountableComponentConnection') -> 'Iterable[_7100.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7100.ShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection))

    def results_for_cvt_belt_connection(self, design_entity: '_1927.CVTBeltConnection') -> 'Iterable[_7043.CVTBeltConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CVTBeltConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CVT_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7043.CVTBeltConnectionCompoundAdvancedSystemDeflection))

    def results_for_belt_connection(self, design_entity: '_1922.BeltConnection') -> 'Iterable[_7012.BeltConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BeltConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BELT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7012.BeltConnectionCompoundAdvancedSystemDeflection))

    def results_for_coaxial_connection(self, design_entity: '_1923.CoaxialConnection') -> 'Iterable[_7027.CoaxialConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CoaxialConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COAXIAL_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7027.CoaxialConnectionCompoundAdvancedSystemDeflection))

    def results_for_connection(self, design_entity: '_1926.Connection') -> 'Iterable[_7038.ConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7038.ConnectionCompoundAdvancedSystemDeflection))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1937.InterMountableComponentConnection') -> 'Iterable[_7068.InterMountableComponentConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.InterMountableComponentConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_INTER_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7068.InterMountableComponentConnectionCompoundAdvancedSystemDeflection))

    def results_for_planetary_connection(self, design_entity: '_1940.PlanetaryConnection') -> 'Iterable[_7086.PlanetaryConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PlanetaryConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PLANETARY_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7086.PlanetaryConnectionCompoundAdvancedSystemDeflection))

    def results_for_rolling_ring_connection(self, design_entity: '_1945.RollingRingConnection') -> 'Iterable[_7096.RollingRingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RollingRingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ROLLING_RING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7096.RollingRingConnectionCompoundAdvancedSystemDeflection))

    def results_for_abstract_shaft_to_mountable_component_connection(self, design_entity: '_1920.AbstractShaftToMountableComponentConnection') -> 'Iterable[_7006.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.AbstractShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ABSTRACT_SHAFT_TO_MOUNTABLE_COMPONENT_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7006.AbstractShaftToMountableComponentConnectionCompoundAdvancedSystemDeflection))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1955.BevelDifferentialGearMesh') -> 'Iterable[_7015.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_DIFFERENTIAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7015.BevelDifferentialGearMeshCompoundAdvancedSystemDeflection))

    def results_for_concept_gear_mesh(self, design_entity: '_1959.ConceptGearMesh') -> 'Iterable[_7033.ConceptGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7033.ConceptGearMeshCompoundAdvancedSystemDeflection))

    def results_for_face_gear_mesh(self, design_entity: '_1965.FaceGearMesh') -> 'Iterable[_7057.FaceGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.FaceGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_FACE_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7057.FaceGearMeshCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1979.StraightBevelDiffGearMesh') -> 'Iterable[_7109.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_DIFF_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7109.StraightBevelDiffGearMeshCompoundAdvancedSystemDeflection))

    def results_for_bevel_gear_mesh(self, design_entity: '_1957.BevelGearMesh') -> 'Iterable[_7020.BevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.BevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7020.BevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_conical_gear_mesh(self, design_entity: '_1961.ConicalGearMesh') -> 'Iterable[_7036.ConicalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConicalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7036.ConicalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1953.AGMAGleasonConicalGearMesh') -> 'Iterable[_7008.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_AGMA_GLEASON_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7008.AGMAGleasonConicalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1963.CylindricalGearMesh') -> 'Iterable[_7051.CylindricalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CylindricalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYLINDRICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7051.CylindricalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1969.HypoidGearMesh') -> 'Iterable[_7066.HypoidGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.HypoidGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7066.HypoidGearMeshCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1972.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_7070.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7070.KlingelnbergCycloPalloidConicalGearMeshCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1973.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_7073.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7073.KlingelnbergCycloPalloidHypoidGearMeshCompoundAdvancedSystemDeflection))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1974.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_7076.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7076.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1977.SpiralBevelGearMesh') -> 'Iterable[_7103.SpiralBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.SpiralBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_SPIRAL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7103.SpiralBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1981.StraightBevelGearMesh') -> 'Iterable[_7112.StraightBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.StraightBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_STRAIGHT_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7112.StraightBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_worm_gear_mesh(self, design_entity: '_1983.WormGearMesh') -> 'Iterable[_7127.WormGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.WormGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_WORM_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7127.WormGearMeshCompoundAdvancedSystemDeflection))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1985.ZerolBevelGearMesh') -> 'Iterable[_7130.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ZerolBevelGearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_ZEROL_BEVEL_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7130.ZerolBevelGearMeshCompoundAdvancedSystemDeflection))

    def results_for_gear_mesh(self, design_entity: '_1967.GearMesh') -> 'Iterable[_7062.GearMeshCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.GearMeshCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_GEAR_MESH](design_entity.wrapped if design_entity else None), constructor.new(_7062.GearMeshCompoundAdvancedSystemDeflection))

    def results_for_cycloidal_disc_central_bearing_connection(self, design_entity: '_1987.CycloidalDiscCentralBearingConnection') -> 'Iterable[_7047.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscCentralBearingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_CENTRAL_BEARING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7047.CycloidalDiscCentralBearingConnectionCompoundAdvancedSystemDeflection))

    def results_for_cycloidal_disc_planetary_bearing_connection(self, design_entity: '_1990.CycloidalDiscPlanetaryBearingConnection') -> 'Iterable[_7049.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.CycloidalDiscPlanetaryBearingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CYCLOIDAL_DISC_PLANETARY_BEARING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7049.CycloidalDiscPlanetaryBearingConnectionCompoundAdvancedSystemDeflection))

    def results_for_ring_pins_to_disc_connection(self, design_entity: '_1993.RingPinsToDiscConnection') -> 'Iterable[_7093.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.cycloidal.RingPinsToDiscConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_RING_PINS_TO_DISC_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7093.RingPinsToDiscConnectionCompoundAdvancedSystemDeflection))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_2000.PartToPartShearCouplingConnection') -> 'Iterable[_7084.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_PART_TO_PART_SHEAR_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7084.PartToPartShearCouplingConnectionCompoundAdvancedSystemDeflection))

    def results_for_clutch_connection(self, design_entity: '_1994.ClutchConnection') -> 'Iterable[_7025.ClutchConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ClutchConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CLUTCH_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7025.ClutchConnectionCompoundAdvancedSystemDeflection))

    def results_for_concept_coupling_connection(self, design_entity: '_1996.ConceptCouplingConnection') -> 'Iterable[_7030.ConceptCouplingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.ConceptCouplingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_CONCEPT_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7030.ConceptCouplingConnectionCompoundAdvancedSystemDeflection))

    def results_for_coupling_connection(self, design_entity: '_1998.CouplingConnection') -> 'Iterable[_7041.CouplingConnectionCompoundAdvancedSystemDeflection]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.advanced_system_deflections.compound.CouplingConnectionCompoundAdvancedSystemDeflection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor.Overloads[_COUPLING_CONNECTION](design_entity.wrapped if design_entity else None), constructor.new(_7041.CouplingConnectionCompoundAdvancedSystemDeflection))

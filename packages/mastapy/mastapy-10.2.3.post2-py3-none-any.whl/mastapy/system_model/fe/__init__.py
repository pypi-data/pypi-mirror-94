'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2007 import AlignConnectedComponentOptions
    from ._2008 import AlignmentMethod
    from ._2009 import AlignmentMethodForRaceBearing
    from ._2010 import AlignmentUsingAxialNodePositions
    from ._2011 import AngleSource
    from ._2012 import BaseFEWithSelection
    from ._2013 import BatchOperations
    from ._2014 import BearingNodeAlignmentOption
    from ._2015 import BearingNodeOption
    from ._2016 import BearingRaceNodeLink
    from ._2017 import BearingRacePosition
    from ._2018 import ComponentOrientationOption
    from ._2019 import ContactPairWithSelection
    from ._2020 import CoordinateSystemWithSelection
    from ._2021 import CreateConnectedComponentOptions
    from ._2022 import DegreeOfFreedomBoundaryCondition
    from ._2023 import DegreeOfFreedomBoundaryConditionAngular
    from ._2024 import DegreeOfFreedomBoundaryConditionLinear
    from ._2025 import ElectricMachineDataSet
    from ._2026 import ElectricMachineDynamicLoadData
    from ._2027 import ElementFaceGroupWithSelection
    from ._2028 import ElementPropertiesWithSelection
    from ._2029 import FEEntityGroupWithSelection
    from ._2030 import FEExportSettings
    from ._2031 import FEPartWithBatchOptions
    from ._2032 import FEStiffnessGeometry
    from ._2033 import FEStiffnessTester
    from ._2034 import FESubstructure
    from ._2035 import FESubstructureExportOptions
    from ._2036 import FESubstructureNode
    from ._2037 import FESubstructureType
    from ._2038 import FESubstructureWithBatchOptions
    from ._2039 import FESubstructureWithSelection
    from ._2040 import FESubstructureWithSelectionComponents
    from ._2041 import FESubstructureWithSelectionForHarmonicAnalysis
    from ._2042 import FESubstructureWithSelectionForModalAnalysis
    from ._2043 import FESubstructureWithSelectionForStaticAnalysis
    from ._2044 import GearMeshingOptions
    from ._2045 import IndependentMastaCreatedCondensationNode
    from ._2046 import LinkComponentAxialPositionErrorReporter
    from ._2047 import LinkNodeSource
    from ._2048 import MaterialPropertiesWithSelection
    from ._2049 import NodeBoundaryConditionStaticAnalysis
    from ._2050 import NodeGroupWithSelection
    from ._2051 import NodeSelectionDepthOption
    from ._2052 import OptionsWhenExternalFEFileAlreadyExists
    from ._2053 import PerLinkExportOptions
    from ._2054 import PerNodeExportOptions
    from ._2055 import RaceBearingFE
    from ._2056 import RaceBearingFESystemDeflection
    from ._2057 import RaceBearingFEWithSelection
    from ._2058 import ReplacedShaftSelectionHelper
    from ._2059 import SystemDeflectionFEExportOptions
    from ._2060 import ThermalExpansionOption

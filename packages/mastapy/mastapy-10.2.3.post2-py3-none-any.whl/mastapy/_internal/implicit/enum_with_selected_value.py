'''enum_with_selected_value.py

Implementations of 'EnumWithSelectedValue' in Python.
As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
'''


from enum import Enum
from typing import List

from mastapy._internal import (
    mixins, enum_with_selected_value_runtime, constructor, conversion
)
from mastapy.shafts import _32, _41
from mastapy._internal.python_net import python_net_import
from mastapy.materials import _65, _69, _55
from mastapy.gears import _136, _134, _137
from mastapy.math_utility import (
    _1084, _1066, _1065, _1080,
    _1079, _1077
)
from mastapy.gears.micro_geometry import (
    _358, _357, _356, _355
)
from mastapy.gears.manufacturing.cylindrical import (
    _406, _405, _409, _391
)
from mastapy.gears.manufacturing.cylindrical.plunge_shaving import _428, _427, _425
from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import _440
from mastapy.geometry.twod.curves import _112
from mastapy.gears.gear_designs.cylindrical import _830, _805, _823
from mastapy.gears.gear_designs.conical import _894, _893, _905
from mastapy.gears.gear_set_pareto_optimiser import _671
from mastapy.utility.model_validation import _1330, _1333
from mastapy.gears.ltca import _607
from mastapy.nodal_analysis import (
    _1409, _1396, _1413, _1402,
    _1381
)
from mastapy.gears.gear_designs.creation_options import _882
from mastapy.gears.gear_designs.bevel import _926, _915
from mastapy.fe_tools.vfx_tools.vfx_enums import _972
from mastapy.bearings.tolerances import (
    _1572, _1583, _1565, _1566,
    _1564
)
from mastapy.detailed_rigid_connectors.splines import (
    _982, _1005, _991, _992,
    _1000, _1006, _983
)
from mastapy.detailed_rigid_connectors.interference_fits import _1036
from mastapy.utility import _1147
from mastapy.utility.report import _1290
from mastapy.nodal_analysis.varying_input_components import _1420
from mastapy.fe_tools.enums import _974
from mastapy.bearings import (
    _1555, _1548, _1556, _1559,
    _1536, _1537, _1561, _1543
)
from mastapy.system_model.part_model import _2075
from mastapy.system_model.drawing.options import _1886
from mastapy.utility.enums import _1356
from mastapy.system_model.imported_fes import (
    _2013, _1974, _2005, _2029
)
from mastapy.system_model import (
    _1838, _1849, _1845, _1847
)
from mastapy.nodal_analysis.fe_export_utility import _1473, _1474
from mastapy.bearings.bearing_results import _1617, _1619, _1618
from mastapy.system_model.part_model.couplings import _2189, _2185, _2188
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3573
from mastapy.system_model.analyses_and_results.static_loads import (
    _6122, _6273, _6202, _6195,
    _6235, _6274
)
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _5040, _5087, _5132, _5157
)
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5391
from mastapy.bearings.bearing_results.rolling.iso_rating_results import _1754
from mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition import _6288

_ARRAY = python_net_import('System', 'Array')
_ENUM_WITH_SELECTED_VALUE = python_net_import('SMT.MastaAPI.Utility.Property', 'EnumWithSelectedValue')


__docformat__ = 'restructuredtext en'
__all__ = (
    'EnumWithSelectedValue_ShaftRatingMethod', 'EnumWithSelectedValue_SurfaceFinishes',
    'EnumWithSelectedValue_LubricantDefinition', 'EnumWithSelectedValue_LubricantViscosityClassISO',
    'EnumWithSelectedValue_MicroGeometryModel', 'EnumWithSelectedValue_ExtrapolationOptions',
    'EnumWithSelectedValue_CylindricalGearRatingMethods', 'EnumWithSelectedValue_LocationOfTipReliefEvaluation',
    'EnumWithSelectedValue_LocationOfRootReliefEvaluation', 'EnumWithSelectedValue_LocationOfEvaluationUpperLimit',
    'EnumWithSelectedValue_LocationOfEvaluationLowerLimit', 'EnumWithSelectedValue_CylindricalMftRoughingMethods',
    'EnumWithSelectedValue_CylindricalMftFinishingMethods', 'EnumWithSelectedValue_MicroGeometryDefinitionType',
    'EnumWithSelectedValue_MicroGeometryDefinitionMethod', 'EnumWithSelectedValue_ChartType',
    'EnumWithSelectedValue_Flank', 'EnumWithSelectedValue_ActiveProcessMethod',
    'EnumWithSelectedValue_CutterFlankSections', 'EnumWithSelectedValue_BasicCurveTypes',
    'EnumWithSelectedValue_ThicknessType', 'EnumWithSelectedValue_ConicalManufactureMethods',
    'EnumWithSelectedValue_ConicalMachineSettingCalculationMethods', 'EnumWithSelectedValue_CandidateDisplayChoice',
    'EnumWithSelectedValue_Severity', 'EnumWithSelectedValue_GeometrySpecificationType',
    'EnumWithSelectedValue_StatusItemSeverity', 'EnumWithSelectedValue_LubricationMethods',
    'EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod', 'EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods',
    'EnumWithSelectedValue_ContactResultType', 'EnumWithSelectedValue_StressResultsType',
    'EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption', 'EnumWithSelectedValue_ToothThicknessSpecificationMethod',
    'EnumWithSelectedValue_LoadDistributionFactorMethods', 'EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods',
    'EnumWithSelectedValue_ProSolveMpcType', 'EnumWithSelectedValue_ITDesignation',
    'EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption', 'EnumWithSelectedValue_SplineRatingTypes',
    'EnumWithSelectedValue_Modules', 'EnumWithSelectedValue_PressureAngleTypes',
    'EnumWithSelectedValue_SplineFitClassType', 'EnumWithSelectedValue_SplineToleranceClassTypes',
    'EnumWithSelectedValue_Table4JointInterfaceTypes', 'EnumWithSelectedValue_ExecutableDirectoryCopier_Option',
    'EnumWithSelectedValue_CadPageOrientation', 'EnumWithSelectedValue_IntegrationMethod',
    'EnumWithSelectedValue_ValueInputOption', 'EnumWithSelectedValue_SinglePointSelectionMethod',
    'EnumWithSelectedValue_ModeInputType', 'EnumWithSelectedValue_MaterialPropertyClass',
    'EnumWithSelectedValue_RollerBearingProfileTypes', 'EnumWithSelectedValue_FluidFilmTemperatureOptions',
    'EnumWithSelectedValue_SupportToleranceLocationDesignation', 'EnumWithSelectedValue_RollingBearingArrangement',
    'EnumWithSelectedValue_RollingBearingRaceType', 'EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod',
    'EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod', 'EnumWithSelectedValue_RotationalDirections',
    'EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing', 'EnumWithSelectedValue_ExcitationAnalysisViewOption',
    'EnumWithSelectedValue_ThreeDViewContourOption', 'EnumWithSelectedValue_LinkNodeSource',
    'EnumWithSelectedValue_ComponentOrientationOption', 'EnumWithSelectedValue_Axis',
    'EnumWithSelectedValue_AlignmentAxis', 'EnumWithSelectedValue_DesignEntityId',
    'EnumWithSelectedValue_ImportedFEType', 'EnumWithSelectedValue_ThermalExpansionOption',
    'EnumWithSelectedValue_BoundaryConditionType', 'EnumWithSelectedValue_FEExportFormat',
    'EnumWithSelectedValue_BearingToleranceClass', 'EnumWithSelectedValue_BearingModel',
    'EnumWithSelectedValue_PreloadType', 'EnumWithSelectedValue_RaceRadialMountingType',
    'EnumWithSelectedValue_RaceAxialMountingType', 'EnumWithSelectedValue_BearingToleranceDefinitionOptions',
    'EnumWithSelectedValue_InternalClearanceClass', 'EnumWithSelectedValue_PowerLoadType',
    'EnumWithSelectedValue_RigidConnectorTypes', 'EnumWithSelectedValue_RigidConnectorStiffnessType',
    'EnumWithSelectedValue_FitTypes', 'EnumWithSelectedValue_RigidConnectorToothSpacingType',
    'EnumWithSelectedValue_DoeValueSpecificationOption', 'EnumWithSelectedValue_AnalysisType',
    'EnumWithSelectedValue_BarModelExportType', 'EnumWithSelectedValue_DynamicsResponseType',
    'EnumWithSelectedValue_DynamicsResponseScaling', 'EnumWithSelectedValue_BearingStiffnessModel',
    'EnumWithSelectedValue_GearMeshStiffnessModel', 'EnumWithSelectedValue_ShaftAndHousingFlexibilityOption',
    'EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType', 'EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput',
    'EnumWithSelectedValue_StressConcentrationMethod', 'EnumWithSelectedValue_MeshStiffnessModel',
    'EnumWithSelectedValue_TorqueRippleInputType', 'EnumWithSelectedValue_HarmonicLoadDataType',
    'EnumWithSelectedValue_HarmonicExcitationType', 'EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification',
    'EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod', 'EnumWithSelectedValue_TorqueSpecificationForSystemDeflection',
    'EnumWithSelectedValue_TorqueConverterLockupRule', 'EnumWithSelectedValue_DegreesOfFreedom',
    'EnumWithSelectedValue_DestinationDesignState'
)


class EnumWithSelectedValue_ShaftRatingMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftRatingMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftRatingMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_32.ShaftRatingMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _32.ShaftRatingMethod

    @classmethod
    def implicit_type(cls) -> '_32.ShaftRatingMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _32.ShaftRatingMethod.type_()

    @property
    def selected_value(self) -> '_32.ShaftRatingMethod':
        '''ShaftRatingMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_32.ShaftRatingMethod]':
        '''List[ShaftRatingMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SurfaceFinishes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SurfaceFinishes

    A specific implementation of 'EnumWithSelectedValue' for 'SurfaceFinishes' types.
    '''

    __hash__ = None
    __qualname__ = 'SurfaceFinishes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_41.SurfaceFinishes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _41.SurfaceFinishes

    @classmethod
    def implicit_type(cls) -> '_41.SurfaceFinishes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _41.SurfaceFinishes.type_()

    @property
    def selected_value(self) -> '_41.SurfaceFinishes':
        '''SurfaceFinishes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_41.SurfaceFinishes]':
        '''List[SurfaceFinishes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricantDefinition(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricantDefinition

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantDefinition' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricantDefinition'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_65.LubricantDefinition':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _65.LubricantDefinition

    @classmethod
    def implicit_type(cls) -> '_65.LubricantDefinition.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _65.LubricantDefinition.type_()

    @property
    def selected_value(self) -> '_65.LubricantDefinition':
        '''LubricantDefinition: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_65.LubricantDefinition]':
        '''List[LubricantDefinition]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricantViscosityClassISO(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricantViscosityClassISO

    A specific implementation of 'EnumWithSelectedValue' for 'LubricantViscosityClassISO' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricantViscosityClassISO'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_69.LubricantViscosityClassISO':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _69.LubricantViscosityClassISO

    @classmethod
    def implicit_type(cls) -> '_69.LubricantViscosityClassISO.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _69.LubricantViscosityClassISO.type_()

    @property
    def selected_value(self) -> '_69.LubricantViscosityClassISO':
        '''LubricantViscosityClassISO: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_69.LubricantViscosityClassISO]':
        '''List[LubricantViscosityClassISO]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryModel

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_136.MicroGeometryModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _136.MicroGeometryModel

    @classmethod
    def implicit_type(cls) -> '_136.MicroGeometryModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _136.MicroGeometryModel.type_()

    @property
    def selected_value(self) -> '_136.MicroGeometryModel':
        '''MicroGeometryModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_136.MicroGeometryModel]':
        '''List[MicroGeometryModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExtrapolationOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExtrapolationOptions

    A specific implementation of 'EnumWithSelectedValue' for 'ExtrapolationOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'ExtrapolationOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1084.ExtrapolationOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1084.ExtrapolationOptions

    @classmethod
    def implicit_type(cls) -> '_1084.ExtrapolationOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1084.ExtrapolationOptions.type_()

    @property
    def selected_value(self) -> '_1084.ExtrapolationOptions':
        '''ExtrapolationOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1084.ExtrapolationOptions]':
        '''List[ExtrapolationOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalGearRatingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalGearRatingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearRatingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearRatingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_55.CylindricalGearRatingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _55.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(cls) -> '_55.CylindricalGearRatingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _55.CylindricalGearRatingMethods.type_()

    @property
    def selected_value(self) -> '_55.CylindricalGearRatingMethods':
        '''CylindricalGearRatingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_55.CylindricalGearRatingMethods]':
        '''List[CylindricalGearRatingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfTipReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfTipReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfTipReliefEvaluation' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfTipReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_358.LocationOfTipReliefEvaluation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _358.LocationOfTipReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_358.LocationOfTipReliefEvaluation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _358.LocationOfTipReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_358.LocationOfTipReliefEvaluation':
        '''LocationOfTipReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_358.LocationOfTipReliefEvaluation]':
        '''List[LocationOfTipReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfRootReliefEvaluation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfRootReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfRootReliefEvaluation' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfRootReliefEvaluation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_357.LocationOfRootReliefEvaluation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _357.LocationOfRootReliefEvaluation

    @classmethod
    def implicit_type(cls) -> '_357.LocationOfRootReliefEvaluation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _357.LocationOfRootReliefEvaluation.type_()

    @property
    def selected_value(self) -> '_357.LocationOfRootReliefEvaluation':
        '''LocationOfRootReliefEvaluation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_357.LocationOfRootReliefEvaluation]':
        '''List[LocationOfRootReliefEvaluation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfEvaluationUpperLimit(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfEvaluationUpperLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationUpperLimit' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfEvaluationUpperLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_356.LocationOfEvaluationUpperLimit':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _356.LocationOfEvaluationUpperLimit

    @classmethod
    def implicit_type(cls) -> '_356.LocationOfEvaluationUpperLimit.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _356.LocationOfEvaluationUpperLimit.type_()

    @property
    def selected_value(self) -> '_356.LocationOfEvaluationUpperLimit':
        '''LocationOfEvaluationUpperLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_356.LocationOfEvaluationUpperLimit]':
        '''List[LocationOfEvaluationUpperLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LocationOfEvaluationLowerLimit(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LocationOfEvaluationLowerLimit

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfEvaluationLowerLimit' types.
    '''

    __hash__ = None
    __qualname__ = 'LocationOfEvaluationLowerLimit'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_355.LocationOfEvaluationLowerLimit':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _355.LocationOfEvaluationLowerLimit

    @classmethod
    def implicit_type(cls) -> '_355.LocationOfEvaluationLowerLimit.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _355.LocationOfEvaluationLowerLimit.type_()

    @property
    def selected_value(self) -> '_355.LocationOfEvaluationLowerLimit':
        '''LocationOfEvaluationLowerLimit: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_355.LocationOfEvaluationLowerLimit]':
        '''List[LocationOfEvaluationLowerLimit]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalMftRoughingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalMftRoughingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftRoughingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalMftRoughingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_406.CylindricalMftRoughingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _406.CylindricalMftRoughingMethods

    @classmethod
    def implicit_type(cls) -> '_406.CylindricalMftRoughingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _406.CylindricalMftRoughingMethods.type_()

    @property
    def selected_value(self) -> '_406.CylindricalMftRoughingMethods':
        '''CylindricalMftRoughingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_406.CylindricalMftRoughingMethods]':
        '''List[CylindricalMftRoughingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalMftFinishingMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalMftFinishingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftFinishingMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalMftFinishingMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_405.CylindricalMftFinishingMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _405.CylindricalMftFinishingMethods

    @classmethod
    def implicit_type(cls) -> '_405.CylindricalMftFinishingMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _405.CylindricalMftFinishingMethods.type_()

    @property
    def selected_value(self) -> '_405.CylindricalMftFinishingMethods':
        '''CylindricalMftFinishingMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_405.CylindricalMftFinishingMethods]':
        '''List[CylindricalMftFinishingMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryDefinitionType

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionType' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryDefinitionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_428.MicroGeometryDefinitionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _428.MicroGeometryDefinitionType

    @classmethod
    def implicit_type(cls) -> '_428.MicroGeometryDefinitionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _428.MicroGeometryDefinitionType.type_()

    @property
    def selected_value(self) -> '_428.MicroGeometryDefinitionType':
        '''MicroGeometryDefinitionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_428.MicroGeometryDefinitionType]':
        '''List[MicroGeometryDefinitionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicroGeometryDefinitionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicroGeometryDefinitionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicroGeometryDefinitionMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'MicroGeometryDefinitionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_427.MicroGeometryDefinitionMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _427.MicroGeometryDefinitionMethod

    @classmethod
    def implicit_type(cls) -> '_427.MicroGeometryDefinitionMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _427.MicroGeometryDefinitionMethod.type_()

    @property
    def selected_value(self) -> '_427.MicroGeometryDefinitionMethod':
        '''MicroGeometryDefinitionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_427.MicroGeometryDefinitionMethod]':
        '''List[MicroGeometryDefinitionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ChartType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ChartType

    A specific implementation of 'EnumWithSelectedValue' for 'ChartType' types.
    '''

    __hash__ = None
    __qualname__ = 'ChartType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_425.ChartType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _425.ChartType

    @classmethod
    def implicit_type(cls) -> '_425.ChartType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _425.ChartType.type_()

    @property
    def selected_value(self) -> '_425.ChartType':
        '''ChartType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_425.ChartType]':
        '''List[ChartType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Flank(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Flank

    A specific implementation of 'EnumWithSelectedValue' for 'Flank' types.
    '''

    __hash__ = None
    __qualname__ = 'Flank'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_409.Flank':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _409.Flank

    @classmethod
    def implicit_type(cls) -> '_409.Flank.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _409.Flank.type_()

    @property
    def selected_value(self) -> '_409.Flank':
        '''Flank: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_409.Flank]':
        '''List[Flank]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ActiveProcessMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ActiveProcessMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ActiveProcessMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ActiveProcessMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_440.ActiveProcessMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _440.ActiveProcessMethod

    @classmethod
    def implicit_type(cls) -> '_440.ActiveProcessMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _440.ActiveProcessMethod.type_()

    @property
    def selected_value(self) -> '_440.ActiveProcessMethod':
        '''ActiveProcessMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_440.ActiveProcessMethod]':
        '''List[ActiveProcessMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CutterFlankSections(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CutterFlankSections

    A specific implementation of 'EnumWithSelectedValue' for 'CutterFlankSections' types.
    '''

    __hash__ = None
    __qualname__ = 'CutterFlankSections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_391.CutterFlankSections':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _391.CutterFlankSections

    @classmethod
    def implicit_type(cls) -> '_391.CutterFlankSections.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _391.CutterFlankSections.type_()

    @property
    def selected_value(self) -> '_391.CutterFlankSections':
        '''CutterFlankSections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_391.CutterFlankSections]':
        '''List[CutterFlankSections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicCurveTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicCurveTypes

    A specific implementation of 'EnumWithSelectedValue' for 'BasicCurveTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicCurveTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_112.BasicCurveTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _112.BasicCurveTypes

    @classmethod
    def implicit_type(cls) -> '_112.BasicCurveTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _112.BasicCurveTypes.type_()

    @property
    def selected_value(self) -> '_112.BasicCurveTypes':
        '''BasicCurveTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_112.BasicCurveTypes]':
        '''List[BasicCurveTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThicknessType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThicknessType

    A specific implementation of 'EnumWithSelectedValue' for 'ThicknessType' types.
    '''

    __hash__ = None
    __qualname__ = 'ThicknessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_830.ThicknessType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _830.ThicknessType

    @classmethod
    def implicit_type(cls) -> '_830.ThicknessType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _830.ThicknessType.type_()

    @property
    def selected_value(self) -> '_830.ThicknessType':
        '''ThicknessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_830.ThicknessType]':
        '''List[ThicknessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ConicalManufactureMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ConicalManufactureMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalManufactureMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalManufactureMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_894.ConicalManufactureMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _894.ConicalManufactureMethods

    @classmethod
    def implicit_type(cls) -> '_894.ConicalManufactureMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _894.ConicalManufactureMethods.type_()

    @property
    def selected_value(self) -> '_894.ConicalManufactureMethods':
        '''ConicalManufactureMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_894.ConicalManufactureMethods]':
        '''List[ConicalManufactureMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ConicalMachineSettingCalculationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ConicalMachineSettingCalculationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ConicalMachineSettingCalculationMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ConicalMachineSettingCalculationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_893.ConicalMachineSettingCalculationMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _893.ConicalMachineSettingCalculationMethods

    @classmethod
    def implicit_type(cls) -> '_893.ConicalMachineSettingCalculationMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _893.ConicalMachineSettingCalculationMethods.type_()

    @property
    def selected_value(self) -> '_893.ConicalMachineSettingCalculationMethods':
        '''ConicalMachineSettingCalculationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_893.ConicalMachineSettingCalculationMethods]':
        '''List[ConicalMachineSettingCalculationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CandidateDisplayChoice(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CandidateDisplayChoice

    A specific implementation of 'EnumWithSelectedValue' for 'CandidateDisplayChoice' types.
    '''

    __hash__ = None
    __qualname__ = 'CandidateDisplayChoice'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_671.CandidateDisplayChoice':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _671.CandidateDisplayChoice

    @classmethod
    def implicit_type(cls) -> '_671.CandidateDisplayChoice.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _671.CandidateDisplayChoice.type_()

    @property
    def selected_value(self) -> '_671.CandidateDisplayChoice':
        '''CandidateDisplayChoice: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_671.CandidateDisplayChoice]':
        '''List[CandidateDisplayChoice]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Severity(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Severity

    A specific implementation of 'EnumWithSelectedValue' for 'Severity' types.
    '''

    __hash__ = None
    __qualname__ = 'Severity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1330.Severity':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1330.Severity

    @classmethod
    def implicit_type(cls) -> '_1330.Severity.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1330.Severity.type_()

    @property
    def selected_value(self) -> '_1330.Severity':
        '''Severity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1330.Severity]':
        '''List[Severity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GeometrySpecificationType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GeometrySpecificationType

    A specific implementation of 'EnumWithSelectedValue' for 'GeometrySpecificationType' types.
    '''

    __hash__ = None
    __qualname__ = 'GeometrySpecificationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_805.GeometrySpecificationType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _805.GeometrySpecificationType

    @classmethod
    def implicit_type(cls) -> '_805.GeometrySpecificationType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _805.GeometrySpecificationType.type_()

    @property
    def selected_value(self) -> '_805.GeometrySpecificationType':
        '''GeometrySpecificationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_805.GeometrySpecificationType]':
        '''List[GeometrySpecificationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StatusItemSeverity(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StatusItemSeverity

    A specific implementation of 'EnumWithSelectedValue' for 'StatusItemSeverity' types.
    '''

    __hash__ = None
    __qualname__ = 'StatusItemSeverity'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1333.StatusItemSeverity':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1333.StatusItemSeverity

    @classmethod
    def implicit_type(cls) -> '_1333.StatusItemSeverity.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1333.StatusItemSeverity.type_()

    @property
    def selected_value(self) -> '_1333.StatusItemSeverity':
        '''StatusItemSeverity: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1333.StatusItemSeverity]':
        '''List[StatusItemSeverity]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LubricationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LubricationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LubricationMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'LubricationMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_134.LubricationMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _134.LubricationMethods

    @classmethod
    def implicit_type(cls) -> '_134.LubricationMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _134.LubricationMethods.type_()

    @property
    def selected_value(self) -> '_134.LubricationMethods':
        '''LubricationMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_134.LubricationMethods]':
        '''List[LubricationMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MicropittingCoefficientOfFrictionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'MicropittingCoefficientOfFrictionCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'MicropittingCoefficientOfFrictionCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_137.MicropittingCoefficientOfFrictionCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _137.MicropittingCoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_137.MicropittingCoefficientOfFrictionCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _137.MicropittingCoefficientOfFrictionCalculationMethod.type_()

    @property
    def selected_value(self) -> '_137.MicropittingCoefficientOfFrictionCalculationMethod':
        '''MicropittingCoefficientOfFrictionCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_137.MicropittingCoefficientOfFrictionCalculationMethod]':
        '''List[MicropittingCoefficientOfFrictionCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingCoefficientOfFrictionMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'ScuffingCoefficientOfFrictionMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_823.ScuffingCoefficientOfFrictionMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _823.ScuffingCoefficientOfFrictionMethods

    @classmethod
    def implicit_type(cls) -> '_823.ScuffingCoefficientOfFrictionMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _823.ScuffingCoefficientOfFrictionMethods.type_()

    @property
    def selected_value(self) -> '_823.ScuffingCoefficientOfFrictionMethods':
        '''ScuffingCoefficientOfFrictionMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_823.ScuffingCoefficientOfFrictionMethods]':
        '''List[ScuffingCoefficientOfFrictionMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ContactResultType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ContactResultType

    A specific implementation of 'EnumWithSelectedValue' for 'ContactResultType' types.
    '''

    __hash__ = None
    __qualname__ = 'ContactResultType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_607.ContactResultType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _607.ContactResultType

    @classmethod
    def implicit_type(cls) -> '_607.ContactResultType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _607.ContactResultType.type_()

    @property
    def selected_value(self) -> '_607.ContactResultType':
        '''ContactResultType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_607.ContactResultType]':
        '''List[ContactResultType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StressResultsType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StressResultsType

    A specific implementation of 'EnumWithSelectedValue' for 'StressResultsType' types.
    '''

    __hash__ = None
    __qualname__ = 'StressResultsType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1409.StressResultsType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1409.StressResultsType

    @classmethod
    def implicit_type(cls) -> '_1409.StressResultsType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1409.StressResultsType.type_()

    @property
    def selected_value(self) -> '_1409.StressResultsType':
        '''StressResultsType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1409.StressResultsType]':
        '''List[StressResultsType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CylindricalGearPairCreationOptions_DerivedParameterOption

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearPairCreationOptions.DerivedParameterOption' types.
    '''

    __hash__ = None
    __qualname__ = 'CylindricalGearPairCreationOptions.DerivedParameterOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_882.CylindricalGearPairCreationOptions.DerivedParameterOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _882.CylindricalGearPairCreationOptions.DerivedParameterOption

    @classmethod
    def implicit_type(cls) -> '_882.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _882.CylindricalGearPairCreationOptions.DerivedParameterOption.type_()

    @property
    def selected_value(self) -> '_882.CylindricalGearPairCreationOptions.DerivedParameterOption':
        '''CylindricalGearPairCreationOptions.DerivedParameterOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_882.CylindricalGearPairCreationOptions.DerivedParameterOption]':
        '''List[CylindricalGearPairCreationOptions.DerivedParameterOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ToothThicknessSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ToothThicknessSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ToothThicknessSpecificationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'ToothThicknessSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_926.ToothThicknessSpecificationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _926.ToothThicknessSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_926.ToothThicknessSpecificationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _926.ToothThicknessSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_926.ToothThicknessSpecificationMethod':
        '''ToothThicknessSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_926.ToothThicknessSpecificationMethod]':
        '''List[ToothThicknessSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LoadDistributionFactorMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LoadDistributionFactorMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LoadDistributionFactorMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'LoadDistributionFactorMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_905.LoadDistributionFactorMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _905.LoadDistributionFactorMethods

    @classmethod
    def implicit_type(cls) -> '_905.LoadDistributionFactorMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _905.LoadDistributionFactorMethods.type_()

    @property
    def selected_value(self) -> '_905.LoadDistributionFactorMethods':
        '''LoadDistributionFactorMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_905.LoadDistributionFactorMethods]':
        '''List[LoadDistributionFactorMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AGMAGleasonConicalGearGeometryMethods

    A specific implementation of 'EnumWithSelectedValue' for 'AGMAGleasonConicalGearGeometryMethods' types.
    '''

    __hash__ = None
    __qualname__ = 'AGMAGleasonConicalGearGeometryMethods'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_915.AGMAGleasonConicalGearGeometryMethods':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _915.AGMAGleasonConicalGearGeometryMethods

    @classmethod
    def implicit_type(cls) -> '_915.AGMAGleasonConicalGearGeometryMethods.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _915.AGMAGleasonConicalGearGeometryMethods.type_()

    @property
    def selected_value(self) -> '_915.AGMAGleasonConicalGearGeometryMethods':
        '''AGMAGleasonConicalGearGeometryMethods: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_915.AGMAGleasonConicalGearGeometryMethods]':
        '''List[AGMAGleasonConicalGearGeometryMethods]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ProSolveMpcType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ProSolveMpcType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveMpcType' types.
    '''

    __hash__ = None
    __qualname__ = 'ProSolveMpcType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_972.ProSolveMpcType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _972.ProSolveMpcType

    @classmethod
    def implicit_type(cls) -> '_972.ProSolveMpcType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _972.ProSolveMpcType.type_()

    @property
    def selected_value(self) -> '_972.ProSolveMpcType':
        '''ProSolveMpcType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_972.ProSolveMpcType]':
        '''List[ProSolveMpcType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ITDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ITDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'ITDesignation' types.
    '''

    __hash__ = None
    __qualname__ = 'ITDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1572.ITDesignation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1572.ITDesignation

    @classmethod
    def implicit_type(cls) -> '_1572.ITDesignation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1572.ITDesignation.type_()

    @property
    def selected_value(self) -> '_1572.ITDesignation':
        '''ITDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1572.ITDesignation]':
        '''List[ITDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DudleyEffectiveLengthApproximationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DudleyEffectiveLengthApproximationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'DudleyEffectiveLengthApproximationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_982.DudleyEffectiveLengthApproximationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _982.DudleyEffectiveLengthApproximationOption

    @classmethod
    def implicit_type(cls) -> '_982.DudleyEffectiveLengthApproximationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _982.DudleyEffectiveLengthApproximationOption.type_()

    @property
    def selected_value(self) -> '_982.DudleyEffectiveLengthApproximationOption':
        '''DudleyEffectiveLengthApproximationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_982.DudleyEffectiveLengthApproximationOption]':
        '''List[DudleyEffectiveLengthApproximationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineRatingTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineRatingTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineRatingTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineRatingTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1005.SplineRatingTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1005.SplineRatingTypes

    @classmethod
    def implicit_type(cls) -> '_1005.SplineRatingTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1005.SplineRatingTypes.type_()

    @property
    def selected_value(self) -> '_1005.SplineRatingTypes':
        '''SplineRatingTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1005.SplineRatingTypes]':
        '''List[SplineRatingTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Modules(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Modules

    A specific implementation of 'EnumWithSelectedValue' for 'Modules' types.
    '''

    __hash__ = None
    __qualname__ = 'Modules'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_991.Modules':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _991.Modules

    @classmethod
    def implicit_type(cls) -> '_991.Modules.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _991.Modules.type_()

    @property
    def selected_value(self) -> '_991.Modules':
        '''Modules: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_991.Modules]':
        '''List[Modules]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PressureAngleTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PressureAngleTypes

    A specific implementation of 'EnumWithSelectedValue' for 'PressureAngleTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'PressureAngleTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_992.PressureAngleTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _992.PressureAngleTypes

    @classmethod
    def implicit_type(cls) -> '_992.PressureAngleTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _992.PressureAngleTypes.type_()

    @property
    def selected_value(self) -> '_992.PressureAngleTypes':
        '''PressureAngleTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_992.PressureAngleTypes]':
        '''List[PressureAngleTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineFitClassType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineFitClassType

    A specific implementation of 'EnumWithSelectedValue' for 'SplineFitClassType' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineFitClassType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1000.SplineFitClassType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1000.SplineFitClassType

    @classmethod
    def implicit_type(cls) -> '_1000.SplineFitClassType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1000.SplineFitClassType.type_()

    @property
    def selected_value(self) -> '_1000.SplineFitClassType':
        '''SplineFitClassType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1000.SplineFitClassType]':
        '''List[SplineFitClassType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SplineToleranceClassTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SplineToleranceClassTypes

    A specific implementation of 'EnumWithSelectedValue' for 'SplineToleranceClassTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'SplineToleranceClassTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1006.SplineToleranceClassTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1006.SplineToleranceClassTypes

    @classmethod
    def implicit_type(cls) -> '_1006.SplineToleranceClassTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1006.SplineToleranceClassTypes.type_()

    @property
    def selected_value(self) -> '_1006.SplineToleranceClassTypes':
        '''SplineToleranceClassTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1006.SplineToleranceClassTypes]':
        '''List[SplineToleranceClassTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Table4JointInterfaceTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Table4JointInterfaceTypes

    A specific implementation of 'EnumWithSelectedValue' for 'Table4JointInterfaceTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'Table4JointInterfaceTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1036.Table4JointInterfaceTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1036.Table4JointInterfaceTypes

    @classmethod
    def implicit_type(cls) -> '_1036.Table4JointInterfaceTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1036.Table4JointInterfaceTypes.type_()

    @property
    def selected_value(self) -> '_1036.Table4JointInterfaceTypes':
        '''Table4JointInterfaceTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1036.Table4JointInterfaceTypes]':
        '''List[Table4JointInterfaceTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExecutableDirectoryCopier_Option(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExecutableDirectoryCopier_Option

    A specific implementation of 'EnumWithSelectedValue' for 'ExecutableDirectoryCopier.Option' types.
    '''

    __hash__ = None
    __qualname__ = 'ExecutableDirectoryCopier.Option'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1147.ExecutableDirectoryCopier.Option':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1147.ExecutableDirectoryCopier.Option

    @classmethod
    def implicit_type(cls) -> '_1147.ExecutableDirectoryCopier.Option.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1147.ExecutableDirectoryCopier.Option.type_()

    @property
    def selected_value(self) -> '_1147.ExecutableDirectoryCopier.Option':
        '''ExecutableDirectoryCopier.Option: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1147.ExecutableDirectoryCopier.Option]':
        '''List[ExecutableDirectoryCopier.Option]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_CadPageOrientation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_CadPageOrientation

    A specific implementation of 'EnumWithSelectedValue' for 'CadPageOrientation' types.
    '''

    __hash__ = None
    __qualname__ = 'CadPageOrientation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1290.CadPageOrientation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1290.CadPageOrientation

    @classmethod
    def implicit_type(cls) -> '_1290.CadPageOrientation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1290.CadPageOrientation.type_()

    @property
    def selected_value(self) -> '_1290.CadPageOrientation':
        '''CadPageOrientation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1290.CadPageOrientation]':
        '''List[CadPageOrientation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_IntegrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_IntegrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'IntegrationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'IntegrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1396.IntegrationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1396.IntegrationMethod

    @classmethod
    def implicit_type(cls) -> '_1396.IntegrationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1396.IntegrationMethod.type_()

    @property
    def selected_value(self) -> '_1396.IntegrationMethod':
        '''IntegrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1396.IntegrationMethod]':
        '''List[IntegrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ValueInputOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ValueInputOption

    A specific implementation of 'EnumWithSelectedValue' for 'ValueInputOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ValueInputOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1413.ValueInputOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1413.ValueInputOption

    @classmethod
    def implicit_type(cls) -> '_1413.ValueInputOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1413.ValueInputOption.type_()

    @property
    def selected_value(self) -> '_1413.ValueInputOption':
        '''ValueInputOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1413.ValueInputOption]':
        '''List[ValueInputOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SinglePointSelectionMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SinglePointSelectionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'SinglePointSelectionMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'SinglePointSelectionMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1420.SinglePointSelectionMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1420.SinglePointSelectionMethod

    @classmethod
    def implicit_type(cls) -> '_1420.SinglePointSelectionMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1420.SinglePointSelectionMethod.type_()

    @property
    def selected_value(self) -> '_1420.SinglePointSelectionMethod':
        '''SinglePointSelectionMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1420.SinglePointSelectionMethod]':
        '''List[SinglePointSelectionMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ModeInputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ModeInputType

    A specific implementation of 'EnumWithSelectedValue' for 'ModeInputType' types.
    '''

    __hash__ = None
    __qualname__ = 'ModeInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1402.ModeInputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1402.ModeInputType

    @classmethod
    def implicit_type(cls) -> '_1402.ModeInputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1402.ModeInputType.type_()

    @property
    def selected_value(self) -> '_1402.ModeInputType':
        '''ModeInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1402.ModeInputType]':
        '''List[ModeInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MaterialPropertyClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MaterialPropertyClass

    A specific implementation of 'EnumWithSelectedValue' for 'MaterialPropertyClass' types.
    '''

    __hash__ = None
    __qualname__ = 'MaterialPropertyClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_974.MaterialPropertyClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _974.MaterialPropertyClass

    @classmethod
    def implicit_type(cls) -> '_974.MaterialPropertyClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _974.MaterialPropertyClass.type_()

    @property
    def selected_value(self) -> '_974.MaterialPropertyClass':
        '''MaterialPropertyClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_974.MaterialPropertyClass]':
        '''List[MaterialPropertyClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollerBearingProfileTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollerBearingProfileTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RollerBearingProfileTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'RollerBearingProfileTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1555.RollerBearingProfileTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1555.RollerBearingProfileTypes

    @classmethod
    def implicit_type(cls) -> '_1555.RollerBearingProfileTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1555.RollerBearingProfileTypes.type_()

    @property
    def selected_value(self) -> '_1555.RollerBearingProfileTypes':
        '''RollerBearingProfileTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1555.RollerBearingProfileTypes]':
        '''List[RollerBearingProfileTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FluidFilmTemperatureOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FluidFilmTemperatureOptions

    A specific implementation of 'EnumWithSelectedValue' for 'FluidFilmTemperatureOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'FluidFilmTemperatureOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1548.FluidFilmTemperatureOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1548.FluidFilmTemperatureOptions

    @classmethod
    def implicit_type(cls) -> '_1548.FluidFilmTemperatureOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1548.FluidFilmTemperatureOptions.type_()

    @property
    def selected_value(self) -> '_1548.FluidFilmTemperatureOptions':
        '''FluidFilmTemperatureOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1548.FluidFilmTemperatureOptions]':
        '''List[FluidFilmTemperatureOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_SupportToleranceLocationDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_SupportToleranceLocationDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'SupportToleranceLocationDesignation' types.
    '''

    __hash__ = None
    __qualname__ = 'SupportToleranceLocationDesignation'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1583.SupportToleranceLocationDesignation':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1583.SupportToleranceLocationDesignation

    @classmethod
    def implicit_type(cls) -> '_1583.SupportToleranceLocationDesignation.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1583.SupportToleranceLocationDesignation.type_()

    @property
    def selected_value(self) -> '_1583.SupportToleranceLocationDesignation':
        '''SupportToleranceLocationDesignation: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1583.SupportToleranceLocationDesignation]':
        '''List[SupportToleranceLocationDesignation]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollingBearingArrangement(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollingBearingArrangement

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingArrangement' types.
    '''

    __hash__ = None
    __qualname__ = 'RollingBearingArrangement'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1556.RollingBearingArrangement':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1556.RollingBearingArrangement

    @classmethod
    def implicit_type(cls) -> '_1556.RollingBearingArrangement.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1556.RollingBearingArrangement.type_()

    @property
    def selected_value(self) -> '_1556.RollingBearingArrangement':
        '''RollingBearingArrangement: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1556.RollingBearingArrangement]':
        '''List[RollingBearingArrangement]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RollingBearingRaceType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RollingBearingRaceType

    A specific implementation of 'EnumWithSelectedValue' for 'RollingBearingRaceType' types.
    '''

    __hash__ = None
    __qualname__ = 'RollingBearingRaceType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1559.RollingBearingRaceType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1559.RollingBearingRaceType

    @classmethod
    def implicit_type(cls) -> '_1559.RollingBearingRaceType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1559.RollingBearingRaceType.type_()

    @property
    def selected_value(self) -> '_1559.RollingBearingRaceType':
        '''RollingBearingRaceType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1559.RollingBearingRaceType]':
        '''List[RollingBearingRaceType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicDynamicLoadRatingCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicDynamicLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1536.BasicDynamicLoadRatingCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1536.BasicDynamicLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1536.BasicDynamicLoadRatingCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1536.BasicDynamicLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1536.BasicDynamicLoadRatingCalculationMethod':
        '''BasicDynamicLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1536.BasicDynamicLoadRatingCalculationMethod]':
        '''List[BasicDynamicLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicStaticLoadRatingCalculationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'BasicStaticLoadRatingCalculationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1537.BasicStaticLoadRatingCalculationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1537.BasicStaticLoadRatingCalculationMethod

    @classmethod
    def implicit_type(cls) -> '_1537.BasicStaticLoadRatingCalculationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1537.BasicStaticLoadRatingCalculationMethod.type_()

    @property
    def selected_value(self) -> '_1537.BasicStaticLoadRatingCalculationMethod':
        '''BasicStaticLoadRatingCalculationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1537.BasicStaticLoadRatingCalculationMethod]':
        '''List[BasicStaticLoadRatingCalculationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RotationalDirections(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RotationalDirections

    A specific implementation of 'EnumWithSelectedValue' for 'RotationalDirections' types.
    '''

    __hash__ = None
    __qualname__ = 'RotationalDirections'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1561.RotationalDirections':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1561.RotationalDirections

    @classmethod
    def implicit_type(cls) -> '_1561.RotationalDirections.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1561.RotationalDirections.type_()

    @property
    def selected_value(self) -> '_1561.RotationalDirections':
        '''RotationalDirections: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1561.RotationalDirections]':
        '''List[RotationalDirections]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftDiameterModificationDueToRollingBearingRing' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftDiameterModificationDueToRollingBearingRing'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2075.ShaftDiameterModificationDueToRollingBearingRing':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2075.ShaftDiameterModificationDueToRollingBearingRing

    @classmethod
    def implicit_type(cls) -> '_2075.ShaftDiameterModificationDueToRollingBearingRing.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2075.ShaftDiameterModificationDueToRollingBearingRing.type_()

    @property
    def selected_value(self) -> '_2075.ShaftDiameterModificationDueToRollingBearingRing':
        '''ShaftDiameterModificationDueToRollingBearingRing: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2075.ShaftDiameterModificationDueToRollingBearingRing]':
        '''List[ShaftDiameterModificationDueToRollingBearingRing]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ExcitationAnalysisViewOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ExcitationAnalysisViewOption

    A specific implementation of 'EnumWithSelectedValue' for 'ExcitationAnalysisViewOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ExcitationAnalysisViewOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1886.ExcitationAnalysisViewOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1886.ExcitationAnalysisViewOption

    @classmethod
    def implicit_type(cls) -> '_1886.ExcitationAnalysisViewOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1886.ExcitationAnalysisViewOption.type_()

    @property
    def selected_value(self) -> '_1886.ExcitationAnalysisViewOption':
        '''ExcitationAnalysisViewOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1886.ExcitationAnalysisViewOption]':
        '''List[ExcitationAnalysisViewOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThreeDViewContourOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThreeDViewContourOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ThreeDViewContourOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1356.ThreeDViewContourOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1356.ThreeDViewContourOption

    @classmethod
    def implicit_type(cls) -> '_1356.ThreeDViewContourOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1356.ThreeDViewContourOption.type_()

    @property
    def selected_value(self) -> '_1356.ThreeDViewContourOption':
        '''ThreeDViewContourOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1356.ThreeDViewContourOption]':
        '''List[ThreeDViewContourOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_LinkNodeSource(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_LinkNodeSource

    A specific implementation of 'EnumWithSelectedValue' for 'LinkNodeSource' types.
    '''

    __hash__ = None
    __qualname__ = 'LinkNodeSource'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2013.LinkNodeSource':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2013.LinkNodeSource

    @classmethod
    def implicit_type(cls) -> '_2013.LinkNodeSource.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2013.LinkNodeSource.type_()

    @property
    def selected_value(self) -> '_2013.LinkNodeSource':
        '''LinkNodeSource: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2013.LinkNodeSource]':
        '''List[LinkNodeSource]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ComponentOrientationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ComponentOrientationOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComponentOrientationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ComponentOrientationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1974.ComponentOrientationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1974.ComponentOrientationOption

    @classmethod
    def implicit_type(cls) -> '_1974.ComponentOrientationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1974.ComponentOrientationOption.type_()

    @property
    def selected_value(self) -> '_1974.ComponentOrientationOption':
        '''ComponentOrientationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1974.ComponentOrientationOption]':
        '''List[ComponentOrientationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_Axis(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_Axis

    A specific implementation of 'EnumWithSelectedValue' for 'Axis' types.
    '''

    __hash__ = None
    __qualname__ = 'Axis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1066.Axis':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1066.Axis

    @classmethod
    def implicit_type(cls) -> '_1066.Axis.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1066.Axis.type_()

    @property
    def selected_value(self) -> '_1066.Axis':
        '''Axis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1066.Axis]':
        '''List[Axis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AlignmentAxis(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AlignmentAxis

    A specific implementation of 'EnumWithSelectedValue' for 'AlignmentAxis' types.
    '''

    __hash__ = None
    __qualname__ = 'AlignmentAxis'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1065.AlignmentAxis':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1065.AlignmentAxis

    @classmethod
    def implicit_type(cls) -> '_1065.AlignmentAxis.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1065.AlignmentAxis.type_()

    @property
    def selected_value(self) -> '_1065.AlignmentAxis':
        '''AlignmentAxis: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1065.AlignmentAxis]':
        '''List[AlignmentAxis]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DesignEntityId(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DesignEntityId

    A specific implementation of 'EnumWithSelectedValue' for 'DesignEntityId' types.
    '''

    __hash__ = None
    __qualname__ = 'DesignEntityId'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1838.DesignEntityId':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1838.DesignEntityId

    @classmethod
    def implicit_type(cls) -> '_1838.DesignEntityId.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1838.DesignEntityId.type_()

    @property
    def selected_value(self) -> '_1838.DesignEntityId':
        '''DesignEntityId: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1838.DesignEntityId]':
        '''List[DesignEntityId]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ImportedFEType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ImportedFEType

    A specific implementation of 'EnumWithSelectedValue' for 'ImportedFEType' types.
    '''

    __hash__ = None
    __qualname__ = 'ImportedFEType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2005.ImportedFEType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2005.ImportedFEType

    @classmethod
    def implicit_type(cls) -> '_2005.ImportedFEType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2005.ImportedFEType.type_()

    @property
    def selected_value(self) -> '_2005.ImportedFEType':
        '''ImportedFEType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2005.ImportedFEType]':
        '''List[ImportedFEType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ThermalExpansionOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ThermalExpansionOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThermalExpansionOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ThermalExpansionOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2029.ThermalExpansionOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2029.ThermalExpansionOption

    @classmethod
    def implicit_type(cls) -> '_2029.ThermalExpansionOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2029.ThermalExpansionOption.type_()

    @property
    def selected_value(self) -> '_2029.ThermalExpansionOption':
        '''ThermalExpansionOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2029.ThermalExpansionOption]':
        '''List[ThermalExpansionOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BoundaryConditionType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BoundaryConditionType

    A specific implementation of 'EnumWithSelectedValue' for 'BoundaryConditionType' types.
    '''

    __hash__ = None
    __qualname__ = 'BoundaryConditionType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1473.BoundaryConditionType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1473.BoundaryConditionType

    @classmethod
    def implicit_type(cls) -> '_1473.BoundaryConditionType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1473.BoundaryConditionType.type_()

    @property
    def selected_value(self) -> '_1473.BoundaryConditionType':
        '''BoundaryConditionType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1473.BoundaryConditionType]':
        '''List[BoundaryConditionType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FEExportFormat(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FEExportFormat

    A specific implementation of 'EnumWithSelectedValue' for 'FEExportFormat' types.
    '''

    __hash__ = None
    __qualname__ = 'FEExportFormat'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1474.FEExportFormat':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1474.FEExportFormat

    @classmethod
    def implicit_type(cls) -> '_1474.FEExportFormat.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1474.FEExportFormat.type_()

    @property
    def selected_value(self) -> '_1474.FEExportFormat':
        '''FEExportFormat: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1474.FEExportFormat]':
        '''List[FEExportFormat]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingToleranceClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingToleranceClass

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceClass' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingToleranceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1565.BearingToleranceClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1565.BearingToleranceClass

    @classmethod
    def implicit_type(cls) -> '_1565.BearingToleranceClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1565.BearingToleranceClass.type_()

    @property
    def selected_value(self) -> '_1565.BearingToleranceClass':
        '''BearingToleranceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1565.BearingToleranceClass]':
        '''List[BearingToleranceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingModel' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1543.BearingModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1543.BearingModel

    @classmethod
    def implicit_type(cls) -> '_1543.BearingModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1543.BearingModel.type_()

    @property
    def selected_value(self) -> '_1543.BearingModel':
        '''BearingModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1543.BearingModel]':
        '''List[BearingModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PreloadType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PreloadType

    A specific implementation of 'EnumWithSelectedValue' for 'PreloadType' types.
    '''

    __hash__ = None
    __qualname__ = 'PreloadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1617.PreloadType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1617.PreloadType

    @classmethod
    def implicit_type(cls) -> '_1617.PreloadType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1617.PreloadType.type_()

    @property
    def selected_value(self) -> '_1617.PreloadType':
        '''PreloadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1617.PreloadType]':
        '''List[PreloadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RaceRadialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RaceRadialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceRadialMountingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RaceRadialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1619.RaceRadialMountingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1619.RaceRadialMountingType

    @classmethod
    def implicit_type(cls) -> '_1619.RaceRadialMountingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1619.RaceRadialMountingType.type_()

    @property
    def selected_value(self) -> '_1619.RaceRadialMountingType':
        '''RaceRadialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1619.RaceRadialMountingType]':
        '''List[RaceRadialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RaceAxialMountingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RaceAxialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceAxialMountingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RaceAxialMountingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1618.RaceAxialMountingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1618.RaceAxialMountingType

    @classmethod
    def implicit_type(cls) -> '_1618.RaceAxialMountingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1618.RaceAxialMountingType.type_()

    @property
    def selected_value(self) -> '_1618.RaceAxialMountingType':
        '''RaceAxialMountingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1618.RaceAxialMountingType]':
        '''List[RaceAxialMountingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingToleranceDefinitionOptions(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingToleranceDefinitionOptions

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceDefinitionOptions' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingToleranceDefinitionOptions'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1566.BearingToleranceDefinitionOptions':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1566.BearingToleranceDefinitionOptions

    @classmethod
    def implicit_type(cls) -> '_1566.BearingToleranceDefinitionOptions.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1566.BearingToleranceDefinitionOptions.type_()

    @property
    def selected_value(self) -> '_1566.BearingToleranceDefinitionOptions':
        '''BearingToleranceDefinitionOptions: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1566.BearingToleranceDefinitionOptions]':
        '''List[BearingToleranceDefinitionOptions]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_InternalClearanceClass(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_InternalClearanceClass

    A specific implementation of 'EnumWithSelectedValue' for 'InternalClearanceClass' types.
    '''

    __hash__ = None
    __qualname__ = 'InternalClearanceClass'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1564.InternalClearanceClass':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1564.InternalClearanceClass

    @classmethod
    def implicit_type(cls) -> '_1564.InternalClearanceClass.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1564.InternalClearanceClass.type_()

    @property
    def selected_value(self) -> '_1564.InternalClearanceClass':
        '''InternalClearanceClass: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1564.InternalClearanceClass]':
        '''List[InternalClearanceClass]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PowerLoadType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PowerLoadType

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadType' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoadType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1849.PowerLoadType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1849.PowerLoadType

    @classmethod
    def implicit_type(cls) -> '_1849.PowerLoadType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1849.PowerLoadType.type_()

    @property
    def selected_value(self) -> '_1849.PowerLoadType':
        '''PowerLoadType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1849.PowerLoadType]':
        '''List[PowerLoadType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2189.RigidConnectorTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2189.RigidConnectorTypes

    @classmethod
    def implicit_type(cls) -> '_2189.RigidConnectorTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2189.RigidConnectorTypes.type_()

    @property
    def selected_value(self) -> '_2189.RigidConnectorTypes':
        '''RigidConnectorTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2189.RigidConnectorTypes]':
        '''List[RigidConnectorTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorStiffnessType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorStiffnessType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorStiffnessType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorStiffnessType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2185.RigidConnectorStiffnessType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2185.RigidConnectorStiffnessType

    @classmethod
    def implicit_type(cls) -> '_2185.RigidConnectorStiffnessType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2185.RigidConnectorStiffnessType.type_()

    @property
    def selected_value(self) -> '_2185.RigidConnectorStiffnessType':
        '''RigidConnectorStiffnessType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2185.RigidConnectorStiffnessType]':
        '''List[RigidConnectorStiffnessType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_FitTypes(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_FitTypes

    A specific implementation of 'EnumWithSelectedValue' for 'FitTypes' types.
    '''

    __hash__ = None
    __qualname__ = 'FitTypes'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_983.FitTypes':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _983.FitTypes

    @classmethod
    def implicit_type(cls) -> '_983.FitTypes.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _983.FitTypes.type_()

    @property
    def selected_value(self) -> '_983.FitTypes':
        '''FitTypes: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_983.FitTypes]':
        '''List[FitTypes]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_RigidConnectorToothSpacingType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_RigidConnectorToothSpacingType

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorToothSpacingType' types.
    '''

    __hash__ = None
    __qualname__ = 'RigidConnectorToothSpacingType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_2188.RigidConnectorToothSpacingType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _2188.RigidConnectorToothSpacingType

    @classmethod
    def implicit_type(cls) -> '_2188.RigidConnectorToothSpacingType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _2188.RigidConnectorToothSpacingType.type_()

    @property
    def selected_value(self) -> '_2188.RigidConnectorToothSpacingType':
        '''RigidConnectorToothSpacingType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_2188.RigidConnectorToothSpacingType]':
        '''List[RigidConnectorToothSpacingType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DoeValueSpecificationOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DoeValueSpecificationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DoeValueSpecificationOption' types.
    '''

    __hash__ = None
    __qualname__ = 'DoeValueSpecificationOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_3573.DoeValueSpecificationOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _3573.DoeValueSpecificationOption

    @classmethod
    def implicit_type(cls) -> '_3573.DoeValueSpecificationOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _3573.DoeValueSpecificationOption.type_()

    @property
    def selected_value(self) -> '_3573.DoeValueSpecificationOption':
        '''DoeValueSpecificationOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_3573.DoeValueSpecificationOption]':
        '''List[DoeValueSpecificationOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_AnalysisType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_AnalysisType

    A specific implementation of 'EnumWithSelectedValue' for 'AnalysisType' types.
    '''

    __hash__ = None
    __qualname__ = 'AnalysisType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6122.AnalysisType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6122.AnalysisType

    @classmethod
    def implicit_type(cls) -> '_6122.AnalysisType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6122.AnalysisType.type_()

    @property
    def selected_value(self) -> '_6122.AnalysisType':
        '''AnalysisType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6122.AnalysisType]':
        '''List[AnalysisType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BarModelExportType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BarModelExportType

    A specific implementation of 'EnumWithSelectedValue' for 'BarModelExportType' types.
    '''

    __hash__ = None
    __qualname__ = 'BarModelExportType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1381.BarModelExportType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1381.BarModelExportType

    @classmethod
    def implicit_type(cls) -> '_1381.BarModelExportType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1381.BarModelExportType.type_()

    @property
    def selected_value(self) -> '_1381.BarModelExportType':
        '''BarModelExportType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1381.BarModelExportType]':
        '''List[BarModelExportType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DynamicsResponseType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DynamicsResponseType

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseType' types.
    '''

    __hash__ = None
    __qualname__ = 'DynamicsResponseType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1080.DynamicsResponseType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1080.DynamicsResponseType

    @classmethod
    def implicit_type(cls) -> '_1080.DynamicsResponseType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1080.DynamicsResponseType.type_()

    @property
    def selected_value(self) -> '_1080.DynamicsResponseType':
        '''DynamicsResponseType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1080.DynamicsResponseType]':
        '''List[DynamicsResponseType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DynamicsResponseScaling(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DynamicsResponseScaling

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseScaling' types.
    '''

    __hash__ = None
    __qualname__ = 'DynamicsResponseScaling'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1079.DynamicsResponseScaling':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1079.DynamicsResponseScaling

    @classmethod
    def implicit_type(cls) -> '_1079.DynamicsResponseScaling.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1079.DynamicsResponseScaling.type_()

    @property
    def selected_value(self) -> '_1079.DynamicsResponseScaling':
        '''DynamicsResponseScaling: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1079.DynamicsResponseScaling]':
        '''List[DynamicsResponseScaling]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_BearingStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_BearingStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'BearingStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5040.BearingStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5040.BearingStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5040.BearingStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5040.BearingStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5040.BearingStiffnessModel':
        '''BearingStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5040.BearingStiffnessModel]':
        '''List[BearingStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearMeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearMeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'GearMeshStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'GearMeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5087.GearMeshStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5087.GearMeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_5087.GearMeshStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5087.GearMeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_5087.GearMeshStiffnessModel':
        '''GearMeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5087.GearMeshStiffnessModel]':
        '''List[GearMeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_ShaftAndHousingFlexibilityOption(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_ShaftAndHousingFlexibilityOption

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftAndHousingFlexibilityOption' types.
    '''

    __hash__ = None
    __qualname__ = 'ShaftAndHousingFlexibilityOption'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5132.ShaftAndHousingFlexibilityOption':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5132.ShaftAndHousingFlexibilityOption

    @classmethod
    def implicit_type(cls) -> '_5132.ShaftAndHousingFlexibilityOption.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5132.ShaftAndHousingFlexibilityOption.type_()

    @property
    def selected_value(self) -> '_5132.ShaftAndHousingFlexibilityOption':
        '''ShaftAndHousingFlexibilityOption: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5132.ShaftAndHousingFlexibilityOption]':
        '''List[ShaftAndHousingFlexibilityOption]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ExportOutputType

    A specific implementation of 'EnumWithSelectedValue' for 'GearWhineAnalysisFEExportOptions.ExportOutputType' types.
    '''

    __hash__ = None
    __qualname__ = 'GearWhineAnalysisFEExportOptions.ExportOutputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5391.GearWhineAnalysisFEExportOptions.ExportOutputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5391.GearWhineAnalysisFEExportOptions.ExportOutputType

    @classmethod
    def implicit_type(cls) -> '_5391.GearWhineAnalysisFEExportOptions.ExportOutputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5391.GearWhineAnalysisFEExportOptions.ExportOutputType.type_()

    @property
    def selected_value(self) -> '_5391.GearWhineAnalysisFEExportOptions.ExportOutputType':
        '''GearWhineAnalysisFEExportOptions.ExportOutputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5391.GearWhineAnalysisFEExportOptions.ExportOutputType]':
        '''List[GearWhineAnalysisFEExportOptions.ExportOutputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_GearWhineAnalysisFEExportOptions_ComplexNumberOutput

    A specific implementation of 'EnumWithSelectedValue' for 'GearWhineAnalysisFEExportOptions.ComplexNumberOutput' types.
    '''

    __hash__ = None
    __qualname__ = 'GearWhineAnalysisFEExportOptions.ComplexNumberOutput'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5391.GearWhineAnalysisFEExportOptions.ComplexNumberOutput':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5391.GearWhineAnalysisFEExportOptions.ComplexNumberOutput

    @classmethod
    def implicit_type(cls) -> '_5391.GearWhineAnalysisFEExportOptions.ComplexNumberOutput.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5391.GearWhineAnalysisFEExportOptions.ComplexNumberOutput.type_()

    @property
    def selected_value(self) -> '_5391.GearWhineAnalysisFEExportOptions.ComplexNumberOutput':
        '''GearWhineAnalysisFEExportOptions.ComplexNumberOutput: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5391.GearWhineAnalysisFEExportOptions.ComplexNumberOutput]':
        '''List[GearWhineAnalysisFEExportOptions.ComplexNumberOutput]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_StressConcentrationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_StressConcentrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'StressConcentrationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'StressConcentrationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1754.StressConcentrationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1754.StressConcentrationMethod

    @classmethod
    def implicit_type(cls) -> '_1754.StressConcentrationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1754.StressConcentrationMethod.type_()

    @property
    def selected_value(self) -> '_1754.StressConcentrationMethod':
        '''StressConcentrationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1754.StressConcentrationMethod]':
        '''List[StressConcentrationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_MeshStiffnessModel(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_MeshStiffnessModel

    A specific implementation of 'EnumWithSelectedValue' for 'MeshStiffnessModel' types.
    '''

    __hash__ = None
    __qualname__ = 'MeshStiffnessModel'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1845.MeshStiffnessModel':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1845.MeshStiffnessModel

    @classmethod
    def implicit_type(cls) -> '_1845.MeshStiffnessModel.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1845.MeshStiffnessModel.type_()

    @property
    def selected_value(self) -> '_1845.MeshStiffnessModel':
        '''MeshStiffnessModel: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1845.MeshStiffnessModel]':
        '''List[MeshStiffnessModel]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueRippleInputType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueRippleInputType

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueRippleInputType' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueRippleInputType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6273.TorqueRippleInputType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6273.TorqueRippleInputType

    @classmethod
    def implicit_type(cls) -> '_6273.TorqueRippleInputType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6273.TorqueRippleInputType.type_()

    @property
    def selected_value(self) -> '_6273.TorqueRippleInputType':
        '''TorqueRippleInputType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6273.TorqueRippleInputType]':
        '''List[TorqueRippleInputType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicLoadDataType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicLoadDataType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicLoadDataType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicLoadDataType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6202.HarmonicLoadDataType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6202.HarmonicLoadDataType

    @classmethod
    def implicit_type(cls) -> '_6202.HarmonicLoadDataType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6202.HarmonicLoadDataType.type_()

    @property
    def selected_value(self) -> '_6202.HarmonicLoadDataType':
        '''HarmonicLoadDataType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6202.HarmonicLoadDataType]':
        '''List[HarmonicLoadDataType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_HarmonicExcitationType(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_HarmonicExcitationType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicExcitationType' types.
    '''

    __hash__ = None
    __qualname__ = 'HarmonicExcitationType'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6195.HarmonicExcitationType':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6195.HarmonicExcitationType

    @classmethod
    def implicit_type(cls) -> '_6195.HarmonicExcitationType.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6195.HarmonicExcitationType.type_()

    @property
    def selected_value(self) -> '_6195.HarmonicExcitationType':
        '''HarmonicExcitationType: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6195.HarmonicExcitationType]':
        '''List[HarmonicExcitationType]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification

    A specific implementation of 'EnumWithSelectedValue' for 'PointLoadLoadCase.ForceSpecification' types.
    '''

    __hash__ = None
    __qualname__ = 'PointLoadLoadCase.ForceSpecification'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6235.PointLoadLoadCase.ForceSpecification':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6235.PointLoadLoadCase.ForceSpecification

    @classmethod
    def implicit_type(cls) -> '_6235.PointLoadLoadCase.ForceSpecification.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6235.PointLoadLoadCase.ForceSpecification.type_()

    @property
    def selected_value(self) -> '_6235.PointLoadLoadCase.ForceSpecification':
        '''PointLoadLoadCase.ForceSpecification: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6235.PointLoadLoadCase.ForceSpecification]':
        '''List[PointLoadLoadCase.ForceSpecification]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_PowerLoadInputTorqueSpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'PowerLoadInputTorqueSpecificationMethod' types.
    '''

    __hash__ = None
    __qualname__ = 'PowerLoadInputTorqueSpecificationMethod'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1847.PowerLoadInputTorqueSpecificationMethod':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1847.PowerLoadInputTorqueSpecificationMethod

    @classmethod
    def implicit_type(cls) -> '_1847.PowerLoadInputTorqueSpecificationMethod.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1847.PowerLoadInputTorqueSpecificationMethod.type_()

    @property
    def selected_value(self) -> '_1847.PowerLoadInputTorqueSpecificationMethod':
        '''PowerLoadInputTorqueSpecificationMethod: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1847.PowerLoadInputTorqueSpecificationMethod]':
        '''List[PowerLoadInputTorqueSpecificationMethod]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueSpecificationForSystemDeflection(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueSpecificationForSystemDeflection

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueSpecificationForSystemDeflection' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueSpecificationForSystemDeflection'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6274.TorqueSpecificationForSystemDeflection':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6274.TorqueSpecificationForSystemDeflection

    @classmethod
    def implicit_type(cls) -> '_6274.TorqueSpecificationForSystemDeflection.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6274.TorqueSpecificationForSystemDeflection.type_()

    @property
    def selected_value(self) -> '_6274.TorqueSpecificationForSystemDeflection':
        '''TorqueSpecificationForSystemDeflection: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6274.TorqueSpecificationForSystemDeflection]':
        '''List[TorqueSpecificationForSystemDeflection]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_TorqueConverterLockupRule(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_TorqueConverterLockupRule

    A specific implementation of 'EnumWithSelectedValue' for 'TorqueConverterLockupRule' types.
    '''

    __hash__ = None
    __qualname__ = 'TorqueConverterLockupRule'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_5157.TorqueConverterLockupRule':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _5157.TorqueConverterLockupRule

    @classmethod
    def implicit_type(cls) -> '_5157.TorqueConverterLockupRule.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _5157.TorqueConverterLockupRule.type_()

    @property
    def selected_value(self) -> '_5157.TorqueConverterLockupRule':
        '''TorqueConverterLockupRule: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_5157.TorqueConverterLockupRule]':
        '''List[TorqueConverterLockupRule]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DegreesOfFreedom(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DegreesOfFreedom

    A specific implementation of 'EnumWithSelectedValue' for 'DegreesOfFreedom' types.
    '''

    __hash__ = None
    __qualname__ = 'DegreesOfFreedom'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_1077.DegreesOfFreedom':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _1077.DegreesOfFreedom

    @classmethod
    def implicit_type(cls) -> '_1077.DegreesOfFreedom.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _1077.DegreesOfFreedom.type_()

    @property
    def selected_value(self) -> '_1077.DegreesOfFreedom':
        '''DegreesOfFreedom: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_1077.DegreesOfFreedom]':
        '''List[DegreesOfFreedom]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None


class EnumWithSelectedValue_DestinationDesignState(mixins.EnumWithSelectedValueMixin, Enum):
    '''EnumWithSelectedValue_DestinationDesignState

    A specific implementation of 'EnumWithSelectedValue' for 'DestinationDesignState' types.
    '''

    __hash__ = None
    __qualname__ = 'DestinationDesignState'

    @classmethod
    def wrapper_type(cls) -> '_ENUM_WITH_SELECTED_VALUE':
        '''Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls) -> '_6288.DestinationDesignState':
        '''Wrapped Pythonnet type of this class.

        Note:
            This property is readonly
        '''

        return _6288.DestinationDesignState

    @classmethod
    def implicit_type(cls) -> '_6288.DestinationDesignState.type_()':
        '''Implicit Pythonnet type of this class.

        Note:
            This property is readonly.
        '''

        return _6288.DestinationDesignState.type_()

    @property
    def selected_value(self) -> '_6288.DestinationDesignState':
        '''DestinationDesignState: 'SelectedValue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

    @property
    def available_values(self) -> 'List[_6288.DestinationDesignState]':
        '''List[DestinationDesignState]: 'AvailableValues' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return None

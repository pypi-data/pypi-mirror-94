'''_2371.py

ShaftSystemDeflection
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.scripting import _6574
from mastapy.system_model.part_model.shaft_model import _2081
from mastapy.system_model.analyses_and_results.static_loads import _6244
from mastapy.system_model.analyses_and_results.power_flows import _3371
from mastapy.system_model.analyses_and_results.system_deflections import _2369, _2370, _2270
from mastapy.shafts import _18
from mastapy.math_utility.measured_vectors import _1134
from mastapy._internal.python_net import python_net_import

_SHAFT_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'ShaftSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('ShaftSystemDeflection',)


class ShaftSystemDeflection(_2270.AbstractShaftOrHousingSystemDeflection):
    '''ShaftSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _SHAFT_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ShaftSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def number_of_cycles_for_fatigue(self) -> 'float':
        '''float: 'NumberOfCyclesForFatigue' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.NumberOfCyclesForFatigue

    @property
    def calculate_outer_diameter_to_achieve_fatigue_safety_factor_requirement(self) -> 'Callable[..., None]':
        '''Callable[..., None]: 'CalculateOuterDiameterToAchieveFatigueSafetyFactorRequirement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateOuterDiameterToAchieveFatigueSafetyFactorRequirement

    @property
    def pin_tangential_oscillation_amplitude(self) -> 'float':
        '''float: 'PinTangentialOscillationAmplitude' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PinTangentialOscillationAmplitude

    @property
    def twod_drawing_showing_axial_forces_with_mounted_components(self) -> '_6574.SMTBitmap':
        '''SMTBitmap: 'TwoDDrawingShowingAxialForcesWithMountedComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6574.SMTBitmap)(self.wrapped.TwoDDrawingShowingAxialForcesWithMountedComponents) if self.wrapped.TwoDDrawingShowingAxialForcesWithMountedComponents else None

    @property
    def component_design(self) -> '_2081.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2081.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6244.ShaftLoadCase':
        '''ShaftLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6244.ShaftLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def power_flow_results(self) -> '_3371.ShaftPowerFlow':
        '''ShaftPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3371.ShaftPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def shaft_section_end_with_worst_static_safety_factor(self) -> '_2369.ShaftSectionEndResultsSystemDeflection':
        '''ShaftSectionEndResultsSystemDeflection: 'ShaftSectionEndWithWorstStaticSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2369.ShaftSectionEndResultsSystemDeflection)(self.wrapped.ShaftSectionEndWithWorstStaticSafetyFactor) if self.wrapped.ShaftSectionEndWithWorstStaticSafetyFactor else None

    @property
    def shaft_section_end_with_worst_fatigue_safety_factor(self) -> '_2369.ShaftSectionEndResultsSystemDeflection':
        '''ShaftSectionEndResultsSystemDeflection: 'ShaftSectionEndWithWorstFatigueSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2369.ShaftSectionEndResultsSystemDeflection)(self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactor) if self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactor else None

    @property
    def shaft_section_end_with_worst_fatigue_safety_factor_for_infinite_life(self) -> '_2369.ShaftSectionEndResultsSystemDeflection':
        '''ShaftSectionEndResultsSystemDeflection: 'ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2369.ShaftSectionEndResultsSystemDeflection)(self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife) if self.wrapped.ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife else None

    @property
    def component_detailed_analysis(self) -> '_18.ShaftDamageResults':
        '''ShaftDamageResults: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_18.ShaftDamageResults)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def planetaries(self) -> 'List[ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(ShaftSystemDeflection))
        return value

    @property
    def shaft_section_results(self) -> 'List[_2370.ShaftSectionSystemDeflection]':
        '''List[ShaftSectionSystemDeflection]: 'ShaftSectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftSectionResults, constructor.new(_2370.ShaftSectionSystemDeflection))
        return value

    @property
    def shaft_section_end_results_by_offset_with_worst_safety_factor(self) -> 'List[_2369.ShaftSectionEndResultsSystemDeflection]':
        '''List[ShaftSectionEndResultsSystemDeflection]: 'ShaftSectionEndResultsByOffsetWithWorstSafetyFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftSectionEndResultsByOffsetWithWorstSafetyFactor, constructor.new(_2369.ShaftSectionEndResultsSystemDeflection))
        return value

    @property
    def mounted_components_applying_torque(self) -> 'List[_1134.ForceResults]':
        '''List[ForceResults]: 'MountedComponentsApplyingTorque' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MountedComponentsApplyingTorque, constructor.new(_1134.ForceResults))
        return value

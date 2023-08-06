'''_5790.py

CylindricalGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2172, _2188
from mastapy._internal import constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5788, _5789, _5801
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5611
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'CylindricalGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetCompoundHarmonicAnalysis',)


class CylindricalGearSetCompoundHarmonicAnalysis(_5801.GearSetCompoundHarmonicAnalysis):
    '''CylindricalGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2172.CylindricalGearSet':
        '''CylindricalGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.CylindricalGearSet.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.ComponentDesign.__class__)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2172.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2172.CylindricalGearSet.TYPE not in self.wrapped.AssemblyDesign.__class__.__mro__:
            raise CastException('Failed to cast assembly_design to CylindricalGearSet. Expected: {}.'.format(self.wrapped.AssemblyDesign.__class__.__qualname__))

        return constructor.new_override(self.wrapped.AssemblyDesign.__class__)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def cylindrical_gears_compound_harmonic_analysis(self) -> 'List[_5788.CylindricalGearCompoundHarmonicAnalysis]':
        '''List[CylindricalGearCompoundHarmonicAnalysis]: 'CylindricalGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsCompoundHarmonicAnalysis, constructor.new(_5788.CylindricalGearCompoundHarmonicAnalysis))
        return value

    @property
    def cylindrical_meshes_compound_harmonic_analysis(self) -> 'List[_5789.CylindricalGearMeshCompoundHarmonicAnalysis]':
        '''List[CylindricalGearMeshCompoundHarmonicAnalysis]: 'CylindricalMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesCompoundHarmonicAnalysis, constructor.new(_5789.CylindricalGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5611.CylindricalGearSetHarmonicAnalysis]':
        '''List[CylindricalGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5611.CylindricalGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5611.CylindricalGearSetHarmonicAnalysis]':
        '''List[CylindricalGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5611.CylindricalGearSetHarmonicAnalysis))
        return value

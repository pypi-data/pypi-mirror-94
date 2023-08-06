'''_5815.py

KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2187
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5813, _5814, _5809
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5655
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis(_5809.KlingelnbergCycloPalloidConicalGearSetCompoundHarmonicAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2187.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2187.KlingelnbergCycloPalloidSpiralBevelGearSet':
        '''KlingelnbergCycloPalloidSpiralBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2187.KlingelnbergCycloPalloidSpiralBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gears_compound_harmonic_analysis(self) -> 'List[_5813.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearsCompoundHarmonicAnalysis, constructor.new(_5813.KlingelnbergCycloPalloidSpiralBevelGearCompoundHarmonicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_meshes_compound_harmonic_analysis(self) -> 'List[_5814.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelMeshesCompoundHarmonicAnalysis, constructor.new(_5814.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5655.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5655.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5655.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5655.KlingelnbergCycloPalloidSpiralBevelGearSetHarmonicAnalysis))
        return value

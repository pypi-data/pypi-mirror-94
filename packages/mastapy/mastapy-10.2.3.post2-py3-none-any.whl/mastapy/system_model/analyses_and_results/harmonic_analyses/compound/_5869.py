'''_5869.py

ZerolBevelGearSetCompoundHarmonicAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2200
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.harmonic_analyses.compound import _5867, _5868, _5759
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5713
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ZerolBevelGearSetCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetCompoundHarmonicAnalysis',)


class ZerolBevelGearSetCompoundHarmonicAnalysis(_5759.BevelGearSetCompoundHarmonicAnalysis):
    '''ZerolBevelGearSetCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2200.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.ZerolBevelGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2200.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2200.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def zerol_bevel_gears_compound_harmonic_analysis(self) -> 'List[_5867.ZerolBevelGearCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearCompoundHarmonicAnalysis]: 'ZerolBevelGearsCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsCompoundHarmonicAnalysis, constructor.new(_5867.ZerolBevelGearCompoundHarmonicAnalysis))
        return value

    @property
    def zerol_bevel_meshes_compound_harmonic_analysis(self) -> 'List[_5868.ZerolBevelGearMeshCompoundHarmonicAnalysis]':
        '''List[ZerolBevelGearMeshCompoundHarmonicAnalysis]: 'ZerolBevelMeshesCompoundHarmonicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesCompoundHarmonicAnalysis, constructor.new(_5868.ZerolBevelGearMeshCompoundHarmonicAnalysis))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_5713.ZerolBevelGearSetHarmonicAnalysis]':
        '''List[ZerolBevelGearSetHarmonicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5713.ZerolBevelGearSetHarmonicAnalysis))
        return value

    @property
    def assembly_harmonic_analysis_load_cases(self) -> 'List[_5713.ZerolBevelGearSetHarmonicAnalysis]':
        '''List[ZerolBevelGearSetHarmonicAnalysis]: 'AssemblyHarmonicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyHarmonicAnalysisLoadCases, constructor.new(_5713.ZerolBevelGearSetHarmonicAnalysis))
        return value

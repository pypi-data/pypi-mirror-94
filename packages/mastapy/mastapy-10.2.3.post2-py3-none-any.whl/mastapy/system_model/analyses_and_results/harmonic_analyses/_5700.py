'''_5700.py

SynchroniserSleeveHarmonicAnalysis
'''


from mastapy.system_model.part_model.couplings import _2251
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6568
from mastapy.system_model.analyses_and_results.system_deflections import _2456
from mastapy.system_model.analyses_and_results.harmonic_analyses import _5699
from mastapy._internal.python_net import python_net_import

_SYNCHRONISER_SLEEVE_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses', 'SynchroniserSleeveHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('SynchroniserSleeveHarmonicAnalysis',)


class SynchroniserSleeveHarmonicAnalysis(_5699.SynchroniserPartHarmonicAnalysis):
    '''SynchroniserSleeveHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _SYNCHRONISER_SLEEVE_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SynchroniserSleeveHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2251.SynchroniserSleeve':
        '''SynchroniserSleeve: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2251.SynchroniserSleeve)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6568.SynchroniserSleeveLoadCase':
        '''SynchroniserSleeveLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6568.SynchroniserSleeveLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

    @property
    def system_deflection_results(self) -> '_2456.SynchroniserSleeveSystemDeflection':
        '''SynchroniserSleeveSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2456.SynchroniserSleeveSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

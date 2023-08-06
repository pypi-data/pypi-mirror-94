'''_5425.py

WormGearHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model.gears import _2197
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6581
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5359
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'WormGearHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearHarmonicAnalysisOfSingleExcitation',)


class WormGearHarmonicAnalysisOfSingleExcitation(_5359.GearHarmonicAnalysisOfSingleExcitation):
    '''WormGearHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2197.WormGear':
        '''WormGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2197.WormGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6581.WormGearLoadCase':
        '''WormGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6581.WormGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

'''_5423.py

UnbalancedMassHarmonicAnalysisOfSingleExcitation
'''


from mastapy.system_model.part_model import _2125
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6579
from mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation import _5424
from mastapy._internal.python_net import python_net_import

_UNBALANCED_MASS_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation', 'UnbalancedMassHarmonicAnalysisOfSingleExcitation')


__docformat__ = 'restructuredtext en'
__all__ = ('UnbalancedMassHarmonicAnalysisOfSingleExcitation',)


class UnbalancedMassHarmonicAnalysisOfSingleExcitation(_5424.VirtualComponentHarmonicAnalysisOfSingleExcitation):
    '''UnbalancedMassHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    '''

    TYPE = _UNBALANCED_MASS_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'UnbalancedMassHarmonicAnalysisOfSingleExcitation.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2125.UnbalancedMass':
        '''UnbalancedMass: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2125.UnbalancedMass)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6579.UnbalancedMassLoadCase':
        '''UnbalancedMassLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6579.UnbalancedMassLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

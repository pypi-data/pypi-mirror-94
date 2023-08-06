'''_3440.py

CycloidalAssemblyStabilityAnalysis
'''


from mastapy.system_model.part_model.cycloidal import _2214
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6455
from mastapy.system_model.analyses_and_results.stability_analyses import _3495
from mastapy._internal.python_net import python_net_import

_CYCLOIDAL_ASSEMBLY_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses', 'CycloidalAssemblyStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CycloidalAssemblyStabilityAnalysis',)


class CycloidalAssemblyStabilityAnalysis(_3495.SpecialisedAssemblyStabilityAnalysis):
    '''CycloidalAssemblyStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYCLOIDAL_ASSEMBLY_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CycloidalAssemblyStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2214.CycloidalAssembly':
        '''CycloidalAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2214.CycloidalAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6455.CycloidalAssemblyLoadCase':
        '''CycloidalAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6455.CycloidalAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

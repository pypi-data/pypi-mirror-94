'''_6237.py

RollingRingAssemblyCriticalSpeedAnalysis
'''


from mastapy.system_model.part_model.couplings import _2243
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6541
from mastapy.system_model.analyses_and_results.critical_speed_analyses import _6244
from mastapy._internal.python_net import python_net_import

_ROLLING_RING_ASSEMBLY_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses', 'RollingRingAssemblyCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('RollingRingAssemblyCriticalSpeedAnalysis',)


class RollingRingAssemblyCriticalSpeedAnalysis(_6244.SpecialisedAssemblyCriticalSpeedAnalysis):
    '''RollingRingAssemblyCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _ROLLING_RING_ASSEMBLY_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RollingRingAssemblyCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def assembly_design(self) -> '_2243.RollingRingAssembly':
        '''RollingRingAssembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2243.RollingRingAssembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6541.RollingRingAssemblyLoadCase':
        '''RollingRingAssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6541.RollingRingAssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

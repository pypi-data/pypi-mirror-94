'''_5107.py

KlingelnbergCycloPalloidSpiralBevelGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2138
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6215
from mastapy.system_model.analyses_and_results.mbd_analyses import _5101
from mastapy._internal.python_net import python_net_import

_KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'KlingelnbergCycloPalloidSpiralBevelGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('KlingelnbergCycloPalloidSpiralBevelGearMultiBodyDynamicsAnalysis',)


class KlingelnbergCycloPalloidSpiralBevelGearMultiBodyDynamicsAnalysis(_5101.KlingelnbergCycloPalloidConicalGearMultiBodyDynamicsAnalysis):
    '''KlingelnbergCycloPalloidSpiralBevelGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _KLINGELNBERG_CYCLO_PALLOID_SPIRAL_BEVEL_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'KlingelnbergCycloPalloidSpiralBevelGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2138.KlingelnbergCycloPalloidSpiralBevelGear':
        '''KlingelnbergCycloPalloidSpiralBevelGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2138.KlingelnbergCycloPalloidSpiralBevelGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6215.KlingelnbergCycloPalloidSpiralBevelGearLoadCase':
        '''KlingelnbergCycloPalloidSpiralBevelGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6215.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

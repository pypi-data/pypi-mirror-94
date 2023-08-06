'''_5075.py

CVTPulleyMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.couplings import _2181
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _5126
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'CVTPulleyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyMultiBodyDynamicsAnalysis',)


class CVTPulleyMultiBodyDynamicsAnalysis(_5126.PulleyMultiBodyDynamicsAnalysis):
    '''CVTPulleyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2181.CVTPulley':
        '''CVTPulley: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CVTPulley)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

'''_3568.py

CVTBeltConnectionCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3537
from mastapy._internal.python_net import python_net_import

_CVT_BELT_CONNECTION_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CVTBeltConnectionCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTBeltConnectionCompoundStabilityAnalysis',)


class CVTBeltConnectionCompoundStabilityAnalysis(_3537.BeltConnectionCompoundStabilityAnalysis):
    '''CVTBeltConnectionCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_BELT_CONNECTION_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTBeltConnectionCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

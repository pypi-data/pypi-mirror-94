'''_3569.py

CVTCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3538
from mastapy._internal.python_net import python_net_import

_CVT_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CVTCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTCompoundStabilityAnalysis',)


class CVTCompoundStabilityAnalysis(_3538.BeltDriveCompoundStabilityAnalysis):
    '''CVTCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

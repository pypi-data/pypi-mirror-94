'''_3570.py

CVTPulleyCompoundStabilityAnalysis
'''


from mastapy.system_model.analyses_and_results.stability_analyses.compound import _3616
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_COMPOUND_STABILITY_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses.Compound', 'CVTPulleyCompoundStabilityAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleyCompoundStabilityAnalysis',)


class CVTPulleyCompoundStabilityAnalysis(_3616.PulleyCompoundStabilityAnalysis):
    '''CVTPulleyCompoundStabilityAnalysis

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_COMPOUND_STABILITY_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleyCompoundStabilityAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

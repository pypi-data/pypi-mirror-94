'''_5776.py

ConnectionCompoundHarmonicAnalysis
'''


from mastapy.system_model.analyses_and_results.analysis_cases import _7136
from mastapy._internal.python_net import python_net_import

_CONNECTION_COMPOUND_HARMONIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound', 'ConnectionCompoundHarmonicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConnectionCompoundHarmonicAnalysis',)


class ConnectionCompoundHarmonicAnalysis(_7136.ConnectionCompoundAnalysis):
    '''ConnectionCompoundHarmonicAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONNECTION_COMPOUND_HARMONIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConnectionCompoundHarmonicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

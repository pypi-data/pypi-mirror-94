'''_6335.py

GearSetCompoundCriticalSpeedAnalysis
'''


from mastapy.system_model.analyses_and_results.critical_speed_analyses.compound import _6373
from mastapy._internal.python_net import python_net_import

_GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.CriticalSpeedAnalyses.Compound', 'GearSetCompoundCriticalSpeedAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetCompoundCriticalSpeedAnalysis',)


class GearSetCompoundCriticalSpeedAnalysis(_6373.SpecialisedAssemblyCompoundCriticalSpeedAnalysis):
    '''GearSetCompoundCriticalSpeedAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_COMPOUND_CRITICAL_SPEED_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetCompoundCriticalSpeedAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

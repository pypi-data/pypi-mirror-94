'''_4777.py

BevelDifferentialPlanetGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2115
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2281
from mastapy.system_model.analyses_and_results.modal_analyses import _4775
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_PLANET_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BevelDifferentialPlanetGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialPlanetGearModalAnalysis',)


class BevelDifferentialPlanetGearModalAnalysis(_4775.BevelDifferentialGearModalAnalysis):
    '''BevelDifferentialPlanetGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_PLANET_GEAR_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialPlanetGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2115.BevelDifferentialPlanetGear':
        '''BevelDifferentialPlanetGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2115.BevelDifferentialPlanetGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2281.BevelDifferentialPlanetGearSystemDeflection':
        '''BevelDifferentialPlanetGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2281.BevelDifferentialPlanetGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

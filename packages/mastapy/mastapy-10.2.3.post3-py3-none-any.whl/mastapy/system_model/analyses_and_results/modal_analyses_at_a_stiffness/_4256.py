'''_4256.py

FaceGearModalAnalysisAtAStiffness
'''


from mastapy.system_model.part_model.gears import _2174
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6481
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import _4261
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'FaceGearModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearModalAnalysisAtAStiffness',)


class FaceGearModalAnalysisAtAStiffness(_4261.GearModalAnalysisAtAStiffness):
    '''FaceGearModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearModalAnalysisAtAStiffness.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def component_design(self) -> '_2174.FaceGear':
        '''FaceGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.FaceGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6481.FaceGearLoadCase':
        '''FaceGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6481.FaceGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None

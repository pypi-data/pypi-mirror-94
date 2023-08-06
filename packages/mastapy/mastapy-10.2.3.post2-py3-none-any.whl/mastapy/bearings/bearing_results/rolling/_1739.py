'''_1739.py

LoadedTaperRollerBearingRow
'''


from mastapy.scripting import _7157
from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling import _1738, _1714
from mastapy._internal.python_net import python_net_import

_LOADED_TAPER_ROLLER_BEARING_ROW = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedTaperRollerBearingRow')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedTaperRollerBearingRow',)


class LoadedTaperRollerBearingRow(_1714.LoadedNonBarrelRollerBearingRow):
    '''LoadedTaperRollerBearingRow

    This is a mastapy class.
    '''

    TYPE = _LOADED_TAPER_ROLLER_BEARING_ROW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedTaperRollerBearingRow.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def major_rib_normal_contact_stress(self) -> '_7157.SMTBitmap':
        '''SMTBitmap: 'MajorRibNormalContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_7157.SMTBitmap)(self.wrapped.MajorRibNormalContactStress) if self.wrapped.MajorRibNormalContactStress else None

    @property
    def loaded_bearing(self) -> '_1738.LoadedTaperRollerBearingResults':
        '''LoadedTaperRollerBearingResults: 'LoadedBearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1738.LoadedTaperRollerBearingResults)(self.wrapped.LoadedBearing) if self.wrapped.LoadedBearing else None

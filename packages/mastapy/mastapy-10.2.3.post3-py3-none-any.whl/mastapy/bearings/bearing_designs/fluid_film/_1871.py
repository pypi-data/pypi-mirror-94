'''_1871.py

PlainOilFedJournalBearing
'''


from mastapy.bearings import _1587
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.bearings.bearing_designs.fluid_film import (
    _1860, _1861, _1862, _1869
)
from mastapy._internal.python_net import python_net_import

_PLAIN_OIL_FED_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainOilFedJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainOilFedJournalBearing',)


class PlainOilFedJournalBearing(_1869.PlainJournalBearing):
    '''PlainOilFedJournalBearing

    This is a mastapy class.
    '''

    TYPE = _PLAIN_OIL_FED_JOURNAL_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlainOilFedJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def feed_type(self) -> '_1587.JournalOilFeedType':
        '''JournalOilFeedType: 'FeedType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.FeedType)
        return constructor.new(_1587.JournalOilFeedType)(value) if value else None

    @feed_type.setter
    def feed_type(self, value: '_1587.JournalOilFeedType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.FeedType = value

    @property
    def land_width(self) -> 'float':
        '''float: 'LandWidth' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.LandWidth

    @property
    def axial_groove_oil_feed(self) -> '_1860.AxialGrooveJournalBearing':
        '''AxialGrooveJournalBearing: 'AxialGrooveOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1860.AxialGrooveJournalBearing)(self.wrapped.AxialGrooveOilFeed) if self.wrapped.AxialGrooveOilFeed else None

    @property
    def axial_hole_oil_feed(self) -> '_1861.AxialHoleJournalBearing':
        '''AxialHoleJournalBearing: 'AxialHoleOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1861.AxialHoleJournalBearing)(self.wrapped.AxialHoleOilFeed) if self.wrapped.AxialHoleOilFeed else None

    @property
    def circumferential_groove_oil_feed(self) -> '_1862.CircumferentialFeedJournalBearing':
        '''CircumferentialFeedJournalBearing: 'CircumferentialGrooveOilFeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1862.CircumferentialFeedJournalBearing)(self.wrapped.CircumferentialGrooveOilFeed) if self.wrapped.CircumferentialGrooveOilFeed else None

'''_6499.py

HarmonicLoadDataJMAGImport
'''


from typing import List

from mastapy.system_model.analyses_and_results.static_loads import _6466, _6498, _6478
from mastapy._internal import constructor, conversion
from mastapy._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_JMAG_IMPORT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'HarmonicLoadDataJMAGImport')


__docformat__ = 'restructuredtext en'
__all__ = ('HarmonicLoadDataJMAGImport',)


class HarmonicLoadDataJMAGImport(_6498.HarmonicLoadDataImportFromMotorPackages['_6478.ElectricMachineHarmonicLoadJMAGImportOptions']):
    '''HarmonicLoadDataJMAGImport

    This is a mastapy class.
    '''

    TYPE = _HARMONIC_LOAD_DATA_JMAG_IMPORT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HarmonicLoadDataJMAGImport.TYPE'):
        super().__init__(instance_to_wrap)
        self._freeze()

    @property
    def electric_machine_data_per_speed(self) -> 'List[_6466.DataFromJMAGPerSpeed]':
        '''List[DataFromJMAGPerSpeed]: 'ElectricMachineDataPerSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ElectricMachineDataPerSpeed, constructor.new(_6466.DataFromJMAGPerSpeed))
        return value

    def select_jmag_file(self):
        ''' 'SelectJMAGFile' is the original name of this method.'''

        self.wrapped.SelectJMAGFile()

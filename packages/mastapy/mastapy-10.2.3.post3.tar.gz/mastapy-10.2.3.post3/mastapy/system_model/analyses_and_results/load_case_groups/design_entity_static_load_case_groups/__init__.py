'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5312 import AbstractAssemblyStaticLoadCaseGroup
    from ._5313 import ComponentStaticLoadCaseGroup
    from ._5314 import ConnectionStaticLoadCaseGroup
    from ._5315 import DesignEntityStaticLoadCaseGroup
    from ._5316 import GearSetStaticLoadCaseGroup
    from ._5317 import PartStaticLoadCaseGroup

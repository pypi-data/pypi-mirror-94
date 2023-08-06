'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1283 import ScriptingSetup
    from ._1284 import UserDefinedPropertyKey
    from ._1285 import UserSpecifiedData

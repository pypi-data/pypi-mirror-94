'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1025 import KeyedJointDesign
    from ._1026 import KeyTypes
    from ._1027 import KeywayJointHalfDesign
    from ._1028 import NumberOfKeys

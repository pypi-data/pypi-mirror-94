'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._975 import DetailedRigidConnectorDesign
    from ._976 import DetailedRigidConnectorHalfDesign

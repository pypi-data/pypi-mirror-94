'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._201 import SpiralBevelGearMeshRating
    from ._202 import SpiralBevelGearRating
    from ._203 import SpiralBevelGearSetRating

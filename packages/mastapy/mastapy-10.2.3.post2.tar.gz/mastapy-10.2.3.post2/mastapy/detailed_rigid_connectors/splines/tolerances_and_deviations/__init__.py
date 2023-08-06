'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1009 import FitAndTolerance
    from ._1010 import SAESplineTolerances

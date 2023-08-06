'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2085 import ConcentricOrParallelPartGroup
    from ._2086 import ConcentricPartGroup
    from ._2087 import ConcentricPartGroupParallelToThis
    from ._2088 import DesignMeasurements
    from ._2089 import ParallelPartGroup
    from ._2090 import PartGroup

'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1950 import ClutchConnection
    from ._1951 import ClutchSocket
    from ._1952 import ConceptCouplingConnection
    from ._1953 import ConceptCouplingSocket
    from ._1954 import CouplingConnection
    from ._1955 import CouplingSocket
    from ._1956 import PartToPartShearCouplingConnection
    from ._1957 import PartToPartShearCouplingSocket
    from ._1958 import SpringDamperConnection
    from ._1959 import SpringDamperSocket
    from ._1960 import TorqueConverterConnection
    from ._1961 import TorqueConverterPumpSocket
    from ._1962 import TorqueConverterTurbineSocket

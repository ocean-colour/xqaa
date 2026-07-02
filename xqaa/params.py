""" Parameters for the XQAA algorithm. """

from dataclasses import dataclass, field


# A small mixin adding introspection helpers shared by the parameter
# dataclasses (field listing, per-field metadata, option checking).
@dataclass
class myDataClass:
    @property
    def fields(self):
        """ Return the list of dataclass field names.

        Returns:
            list: The names of every field on this dataclass.
        """
        return list(self.__dataclass_fields__.keys())

    def meta(self, attribute_name: str):
        """ Return the metadata dict for a given field.

        Parameters:
            attribute_name (str): Name of the field.

        Returns:
            dict: The ``metadata`` mapping declared for that field.
        """
        return self.__dataclass_fields__[attribute_name].metadata

    def chk_options(self, attribute_name: str):
        """ Check whether a field's current value is one of its allowed options.

        Parameters:
            attribute_name (str): Name of the field to validate. The field
                must declare an ``options`` list in its metadata.

        Returns:
            bool: True if the current value is in the allowed ``options``.
        """
        options = self.__dataclass_fields__[attribute_name].metadata['options']
        return getattr(self, attribute_name) in options


@dataclass
class XQAAParams(myDataClass):
    """ Configuration for an XQAA retrieval.

    Groups the wavelength windows, the non-water backscatter correction
    scheme, and the reference dataset / variant used to load the QSSA
    G-coefficients.
    """
    bbmin: float = field(
        default=600.0,
        metadata={
            "help": "Minimum wavelength for the bbp averaging window",
            "unit": "nm",
            "Notation": "b_{\\rm b,min}",
        },
    )
    bbmax: float = field(
        default=650.0,
        metadata={
            "help": "Maximum wavelength for the bbp averaging window",
            "unit": "nm",
            "Notation": "b_{\\rm b,max}",
        },
    )
    bbp_corr: str = field(
        default="pow",
        metadata={
            "help": "Correction scheme for the particulate backscatter (bbp)",
            "options": ["none", "mean", "pow"],
        },
    )
    amin: float = field(
        default=400.0,
        metadata={
            "help": "Minimum wavelength for absorption coefficient",
            "unit": "nm",
            "Notation": "a_{\\rm min}",
        },
    )
    amax: float = field(
        default=450.0,
        metadata={
            "help": "Maximum wavelength for absorption coefficient",
            "unit": "nm",
            "Notation": "a_{\\rm max}",
        },
    )
    dataset: str = field(
        default="loisel23",
        metadata={
            "help": "Dataset to use for the inversion",
            "options": ["loisel23"],
        },
    )
    L23_X: int = field(
        default=4,
        metadata={
            "help": "X index for Loisel23 dataset",
            "Notation": "X",
        },
    )
    L23_Y: int = field(
        default=0,
        metadata={
            "help": "Y index for Loisel23 dataset",
            "Notation": "Y",
        },
    )

import weakref
from dataclasses import field
from typing import Any, Dict, List, Optional, Union

from pydantic import validator

from ome_types import util
from ome_types.dataclasses import ome_dataclass

from .annotation import Annotation
from .boolean_annotation import BooleanAnnotation
from .comment_annotation import CommentAnnotation
from .dataset import Dataset
from .double_annotation import DoubleAnnotation
from .experiment import Experiment
from .experimenter import Experimenter
from .experimenter_group import ExperimenterGroup
from .file_annotation import FileAnnotation
from .folder import Folder
from .image import Image
from .instrument import Instrument
from .list_annotation import ListAnnotation
from .long_annotation import LongAnnotation
from .map_annotation import MapAnnotation
from .plate import Plate
from .project import Project
from .rights import Rights
from .roi import ROI
from .screen import Screen
from .simple_types import UniversallyUniqueIdentifier
from .tag_annotation import TagAnnotation
from .term_annotation import TermAnnotation
from .timestamp_annotation import TimestampAnnotation
from .xml_annotation import XMLAnnotation

_annotation_types: Dict[str, type] = {
    "boolean_annotation": BooleanAnnotation,
    "comment_annotation": CommentAnnotation,
    "double_annotation": DoubleAnnotation,
    "file_annotation": FileAnnotation,
    "list_annotation": ListAnnotation,
    "long_annotation": LongAnnotation,
    "map_annotation": MapAnnotation,
    "tag_annotation": TagAnnotation,
    "term_annotation": TermAnnotation,
    "timestamp_annotation": TimestampAnnotation,
    "xml_annotation": XMLAnnotation,
}


@ome_dataclass
class BinaryOnly:
    """Pointer to an external metadata file.

    If this              element is present, then no other metadata may be present
    in this              file, i.e. this file is a place-holder.

    Parameters
    ----------
    metadata_file : str
        Filename of the OME-XML metadata file for                  this binary
        data. If the file cannot be found, a search can                  be
        performed based on the UUID.
    uuid : UniversallyUniqueIdentifier
        The unique identifier of another OME-XML                  block whose
        metadata describes the binary data in this file.                  This
        UUID is considered authoritative regardless of
        mismatches in the filename.
    """

    metadata_file: str
    uuid: UniversallyUniqueIdentifier


@ome_dataclass
class OME:
    """The OME element is a container for all information objects accessible by OME.

    These information objects include descriptions of the imaging experiments and
    the people who perform them, descriptions of the microscope, the resulting
    images and how they were acquired, the analyses performed on those images, and
    the analysis results themselves. An OME file may contain any or all of this
    information.

    With the creation of the Metadata Only Companion OME-XML and Binary Only OME-
    TIFF files the top level OME node has changed slightly. It can EITHER: Contain
    all the previously expected elements OR: Contain a single BinaryOnly element
    that points at its Metadata Only Companion OME-XML file.

    Parameters
    ----------
    binary_only : BinaryOnly, optional
        Pointer to an external metadata file. If this              element is
        present, then no other metadata may be present in this
        file, i.e. this file is a place-holder.
    creator : str, optional
        This is the name of the creating application of the OME-XML and
        preferably its full version. e.g "CompanyName, SoftwareName,
        V2.6.3456" This is optional but we hope it will be set by applications
        writing out OME-XML from scratch.
    datasets : Dataset, optional
    experimenter_groups : ExperimenterGroup, optional
    experimenters : Experimenter, optional
    experiments : Experiment, optional
    folders : Folder, optional
    images : Image, optional
    instruments : Instrument, optional
    plates : Plate, optional
    projects : Project, optional
    rights : Rights, optional
    rois : ROI, optional
    screens : Screen, optional
    structured_annotations : List[Annotation], optional
    uuid : UniversallyUniqueIdentifier, optional
        This unique identifier is used to keep track of multi part files. It
        allows the links between files to survive renaming.  While OPTIONAL in
        the general case this is REQUIRED in a MetadataOnly Companion to a
        collection of BinaryOnly files.
    """

    binary_only: Optional[BinaryOnly] = None
    creator: Optional[str] = None
    datasets: List[Dataset] = field(default_factory=list)
    experimenter_groups: List[ExperimenterGroup] = field(default_factory=list)
    experimenters: List[Experimenter] = field(default_factory=list)
    experiments: List[Experiment] = field(default_factory=list)
    folders: List[Folder] = field(default_factory=list)
    images: List[Image] = field(default_factory=list)
    instruments: List[Instrument] = field(default_factory=list)
    plates: List[Plate] = field(default_factory=list)
    projects: List[Project] = field(default_factory=list)
    rights: Optional[Rights] = None
    rois: List[ROI] = field(default_factory=list)
    screens: List[Screen] = field(default_factory=list)
    structured_annotations: List[Annotation] = field(default_factory=list)
    uuid: Optional[UniversallyUniqueIdentifier] = None

    def __post_init_post_parse__(self: Any, *args: Any) -> None:
        self._link_refs()

    def _link_refs(self):
        ids = util.collect_ids(self)
        for ref in util.collect_references(self):
            ref.ref_ = weakref.ref(ids[ref.id])

    def __setstate__(self: Any, state: Dict[str, Any]) -> None:
        """Support unpickle of our weakref references."""
        self.__dict__.update(state)
        self._link_refs()

    @validator("structured_annotations", pre=True, each_item=True)
    def validate_structured_annotations(
        cls, value: Union[Annotation, Dict[Any, Any]]
    ) -> Annotation:
        if isinstance(value, Annotation):
            return value
        elif isinstance(value, dict):
            try:
                _type = value.pop("_type")
            except KeyError:
                raise ValueError("dict initialization requires _type") from None
            try:
                annotation_cls = _annotation_types[_type]
            except KeyError:
                raise ValueError(f"unknown Annotation type '{_type}'") from None
            return annotation_cls(**value)
        else:
            raise ValueError("invalid type for annotation values")

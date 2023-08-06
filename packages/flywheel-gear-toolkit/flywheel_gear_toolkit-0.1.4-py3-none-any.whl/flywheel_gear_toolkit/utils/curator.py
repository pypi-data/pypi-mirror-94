import abc
import importlib
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import flywheel

from flywheel_gear_toolkit import GearToolkitContext
from flywheel_gear_toolkit.utils.datatypes import Container, PathLike


def _load_curator(curator_path: PathLike):
    """Load curator from the file, return the module.

    Args:
        curator_path (Path-like): Path to curator script.

    Returns:
        (module): A python module.
    """
    if isinstance(curator_path, str):
        curator_path = Path(curator_path).resolve()
    if curator_path.is_file():
        old_syspath = sys.path[:]
        try:
            sys.path.append(str(curator_path.parent))
            ## Investigate import statement
            mod = importlib.import_module(curator_path.name.split(".")[0])
            mod.filename = str(curator_path)
        finally:
            sys.path = old_syspath
    else:
        mod = None

    return mod


def get_curator(
    context: GearToolkitContext,
    curator_path: PathLike,
    write_report: bool = False,
    **kwargs,
):
    """Returns an instantiated curator

    Args:
        client (flywheel.Client): The flywheel sdk client.
        curator_path (Path-like): A path to a curator module.
        **kwargs: Extra keyword arguments.
    """
    curator_mod = _load_curator(curator_path)
    curator = curator_mod.Curator(
        context=context, write_report=write_report, **kwargs
    )

    return curator


class Curator(abc.ABC):
    """Base abstract class for the HierarchyCurator and FileCurator

    Implements an init function and declares the abstract method curate_container

    FileCurator is meant to be implemented for use in a utility gear that acts on input files in a gear rule

    HierarchyCurator is meant to be implemented for use in an analysis gear that curates an input hierarchy.

    Args:
        kwargs (Dict[str,Any], optional): Dictionary of attributes to set in class
    """

    def __init__(self, **kwargs: Optional[Dict[str, Any]]) -> None:
        """An abstract class to be implemented in the input python file."""

        self.depth_first = True
        self.optional_requirements = None
        self.input_file_one = None
        self.input_file_two = None
        self.input_file_three = None
        self.context = None
        self.client = None
        self.write_report = True

        for k, v in kwargs.items():
            setattr(self, k, v)

    @abc.abstractmethod
    def curate_container(
        self, container: Union[Container, Dict[str, Any]]
    ):  # pragma: no cover
        """Curates a generic container.

        Args:
            container (Container or dict): A Flywheel container or its dictionary representation.
        """
        raise NotImplementedError


class HierarchyCurator(Curator):
    """An abstract class that user-defined Curator class should inherited from.

    This class defines abstract methods for each container type (e.g `curate_project`) (i.e. methods that need to be defined in the child curator Class implemented by the user, see example scripts in the example folder). Such method is decorated with the `abc.abstractmethod` decorator in this abstract class.

    Validation methods are also defined for each container types. Validation methods become handy when, for example, curating a file is a time consuming process: it allows for marking a file during the curation method and check for that mark elsewhere in the validate method.

    Example:

    .. code-block:: python

        from custom_curator import curator
        class Curator(curator.Curator):

        def curate_file(self, file_):
        # Curates a file by setting the field 'file.info.curated' to True
        file_.update_info({'curated': True})

        def validate_file(self, file_):
            # Returns True if file needs curation, False otherwise
            return not file_.info.get('curated', False)
    """

    def curate_container(self, container: Container):
        """Curates a generic container.

        Args:
            container (Container): A Flywheel container.
        """
        if hasattr(container, "container_type"):
            container_type = container.container_type
            if container_type == "project":
                if self.validate_project(container):
                    self.curate_project(container)
            elif container_type == "subject":
                if self.validate_subject(container):
                    self.curate_subject(container)
            elif container_type == "session":
                if self.validate_session(container):
                    self.curate_session(container)
            elif container_type == "acquisition":
                if self.validate_acquisition(container):
                    self.curate_acquisition(container)
            elif container_type == "file":
                if self.validate_file(container):
                    self.curate_file(container)
            else:
                if self.validate_analysis(container):
                    self.curate_analysis(container)
        else:
            # element is a file and has no children
            if self.validate_file(container):
                self.curate_file(container)

    def curate_project(self, project: flywheel.Project):  # pragma: no cover
        """Curates a project.

        Args:
            project (flywheel.Project): The project object to curate
        """
        pass

    def curate_subject(self, subject: flywheel.Subject):  # pragma: no cover
        """Curates a subject.

        Args:
            subject (flywheel.Subject): The subject object to curate
        """
        pass

    def curate_session(self, session: flywheel.Session):  # pragma: no cover
        """Curates a session.

        Args:
            session (flywheel.Session): The session object to curate
        """
        pass

    def curate_acquisition(
        self, acquisition: flywheel.Acquisition
    ):  # pragma: no cover
        """Curates an acquisition.

        Args:
            acquisition (flywheel.Acquisition): The acquisition object to
                curate
        """
        pass

    def curate_analysis(
        self, analysis: flywheel.AnalysisOutput
    ):  # pragma: no cover
        """Curates an analysis.

        Args:
            analysis (flywheel.Analysis): The analysis object to curate
        """
        pass

    def curate_file(self, file_: flywheel.FileEntry):  # pragma: no cover
        """Curates a file.

        Args:
            file_ (flywheel.FileEntry): The file entry object to curate
        """
        pass

    def validate_project(self, project: flywheel.Project):  # pragma: no cover
        """Returns True if a project needs curation, False otherwise.

        Args:
            project (flywheel.Project): The project object to validate

        Returns:
            bool: Whether or not the project is curated correctly
        """
        return True

    def validate_subject(self, subject: flywheel.Subject):  # pragma: no cover
        """Returns True if a subject needs curation, False otherwise.

        Args:
            subject (flywheel.Subject): The subject object to validate

        Returns:
            bool: Whether or not the subject is curated correctly
        """
        return True

    def validate_session(self, session: flywheel.Session):  # pragma: no cover
        """Returns True if a session needs curation, False otherwise.

        Args:
            session (flywheel.Session): The session object to validate

        Returns:
            bool: Whether or not the session is curated correctly
        """
        return True

    def validate_acquisition(
        self, acquisition: flywheel.Acquisition
    ):  # pragma: no cover
        """Returns True if a acquisition needs curation, False otherwise.

        Args:
            acquisition (flywheel.Acquisition): The acquisition object to
                validate

        Returns:
            bool: Whether or not the acquisition is curated correctly
        """
        return True

    def validate_analysis(
        self, analysis: flywheel.AnalysisOutput
    ):  # pragma: no cover
        """Returns True if a analysis needs curation, False otherwise.

        Args:
            analysis (flywheel.Analysis): The analysis object to validate

        Returns:
            bool: Whether or not the analysis is curated correctly
        """
        return True

    def validate_file(self, file_: flywheel.FileEntry):  # pragma: no cover
        """Returns True if a file_ needs curation, False otherwise.

        Args:
            file_ (flywheel.FileEntry): The file entry object to validate

        Returns:
            bool: Whether or not the file_ is curated correctly
        """
        return True


class FileCurator(Curator):
    def curate_container(
        self, container: Union[Container, Dict[str, Any]]
    ) -> None:
        """Curates a generic container.
        Args:
            container (Dict or Container): A Flywheel file.
        """
        if self.validate_file(container):
            self.curate_file(container)

    def curate_file(
        self, file_: Union[flywheel.FileEntry, Dict[str, Any]]
    ) -> None:  # pragma: no cover
        """Curates a file.

        Args:
            file_ (Dict or flywheel.FileEntry):
                The file entry object to curate
        """
        pass

    def validate_file(
        self, file_: Union[flywheel.FileEntry, Dict[str, Any]]
    ) -> bool:  # pragma: no cover
        """Returns True if a file_ needs curation, False otherwise.

        Args:
            file_ (Dict or flywheel.FileEntry):
                The file entry object to validate

        Returns:
            bool: Whether or not the file_ is curated correctly
        """
        return True

"""A module to store reporter classes"""
import csv
import dataclasses
import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

from flywheel_gear_toolkit.utils import datatypes

log = logging.getLogger(__name__)


@dataclasses.dataclass
class BaseLogRecord:
    """Base class for creating log record formats

    This class should be subclassed and fields added to create a log record format.
    The subclass can either define default values for the fields created, or not.
    If default values are defined, then the reporter will warn when keys are left
    unset, but if default values are not defined, the reporter will error and exit
    if a key is not set.

    Raises:
        TypeError:
            1. If the type definition and the assigned type mismatch
            2. If no defualt values are defined in the subclass and no values are
                provided in the __init__() method
    """

    # Enforce declared types
    def __post_init__(self):
        for (name, field_type) in self.__annotations__.items():
            cur_attr = getattr(self, name)
            if not isinstance(cur_attr, field_type):
                cur_type = type(cur_attr)
                raise TypeError(
                    f"The field '{name}' was assigned type '{cur_type}' instead of '{field_type}'"
                )

    @classmethod
    def keys(cls):
        return cls.__dataclass_fields__.keys()

    def values(self):
        return dataclasses.astuple(self)

    def to_dict(self):
        return dataclasses.asdict(self)

    def items(self):
        return self.to_dict().items()


@dataclasses.dataclass
class LogRecord(BaseLogRecord):
    """
    Args:
        container_type (str, optional): Container type. Defaults to "".
        container_id (str, optional): Container id. Defaults to "".
        label (str, optional): Container label. Defaults to "".
        err (str, optional): Error message. Defaults to "".
        msg (str, optional): Other message. Defaults to "".
        resolved (bool, optional): Resolved or not. Defaults to False.
        search_key (str, optional): Search keyword. Defaults to "".
    """

    container_type: str = ""
    container_id: str = ""
    label: str = ""
    err: str = ""
    msg: str = ""
    resolved: bool = False
    search_key: str = ""


# TODO: Make Curator reorter into a reporter for an analysis gear that can upload a log to each container it curates


class AggregatedReporter:
    """
    Creates an aggregated reporter and outputs it in CSV or JSON format.

    This reporter can be used in any gear to create a file report for the actions the gear has taken or any errors that need to be reported.

    For the Hierarchy Curator, AggregatedReporter object should be instantiated in the top level container curation method and saved as one of Curator's attributes.

    Example: If you want to curate all the sessions in a subject, and log any error that raises during session curation

    .. code-block:: python

        from flywheel_gear_toolkit import GearToolkitContext
        from flywheel_gear_toolkit.utils import curator

        class Curator(curator.HierarchyCurator):

            def __init__(self):
                super().__init__(depth_first=True)
                self.reporter = None

            def curate_subject(self, subject):
                self.reporter = AggregatedReporter(
                    output_dir=gear_context.output_dir,
                    container_label=subject.label
                )

            def curate_session(self, session):
                try:
                    # something that may raise
                except Exception as exc:
                    self.reporter.append_log(
                        c_type: 'session',
                        label: session.label,
                        c_id: session.id
                        resolved: "False",
                        err: exc.message
                    )

        Args:
            output_path (str, Path.or os.path):  Path to where the output report file will be saved, output type is inferred by extension
            format (class): Dataclass representing log entry fields
                The class must subclass BaseLogRecord,
                i.e. issubclass(log_format, BaseLogRecord) == True

        Raises:
            ValueError: When output type cannot be inferred or log_format doesn't subclass BaseLogRecord
            TypeError: If log_format is not a subclass of BaseLogRecord
    """

    def __init__(
        self,
        output_path: datatypes.PathLike,
        format: Type[BaseLogRecord] = LogRecord,
    ) -> None:
        self.output_path = Path(output_path)
        self.file_cursor = None
        self.csv_writer = None
        self.first_record = True
        self.output_type = self.output_path.suffix[1:]
        self.format = format

        if not issubclass(self.format, BaseLogRecord):
            raise TypeError("Log format must be a subclass of BaseLogRecord")

        self.keys = self.format.keys()

        if not self.keys:
            raise ValueError(
                f"No fields found in log format class {self.format.__name__}, please ensure to include the '@dataclasses.dataclass' decorator over the class definition."
            )

        if self.output_type not in ["csv", "json"]:
            raise ValueError(
                "Only output types of CSV and JSON are currently supported"
            )

        if self.output_path.exists():
            raise ValueError("Log path exists already, won't overwrite")

        self.file_cursor = open(self.output_path, "w", encoding="utf-8")

        if self.output_type == "csv":
            # Create the output csv file
            log.info(
                f"CSV file selected, writing header to '{self.output_path}'"
            )
            self.csv_writer = csv.DictWriter(
                self.file_cursor, fieldnames=list(self.keys)
            )
            self.csv_writer.writeheader()
        else:
            # For JSON, the class writes a list of JSON objects to the file.
            #   Straight appending won't work because the objects need to be
            #   wrapped in a list.  This method starts the file with an opening
            #   list and closes the file with a closing bracket to make the
            #   resulting file valid json.

            # As consequence, the file will not be valid JSON until the
            #   destructor is called.

            log.info(f"Touching JSON output '{self.output_path}'")
            self.file_cursor.write("[\n")

    def __del__(self):
        """
        Write footer for json and close the file
        """
        if self.file_cursor and not self.file_cursor.closed:
            if self.output_type == "json":
                self.file_cursor.write("]")
            self.file_cursor.close()

    def append_log(
        self,
        record: Optional[BaseLogRecord] = None,
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        """Add a message to the report.  Either an instance of self.format can be passed, or keyword arguments, but not both.

        If kwargs are passed, only keys that are in self.format.keys() will be populated.  If not all keys are passed in, one of two things will happen:
            1. If self.format has defaults, a warning will be logged to the console
            2. If self.format doesn't have defaults, a ValueError will be raised

        These two functionalities allow for the optional enforcing of all keys to be populated, or enforcing certain keys be populated and making others optional.

        Args:
            record (BaseLogRecord, optional): Instance of self.format. Defaults to None
            kwargs (Dict[str,Any], optional): Dictionary or keyword arguments that will be inserted.  Only fields matching what is defined in self.format will be populated. Declared types will be enforced. Defaults to None

        Raises:
            ValueError: If both a record object and keyword arguments are passed
        """
        if record:
            rec = record
            if kwargs:
                raise ValueError(
                    "Can only pass a log_record instance, or keyword arguments, not both."
                )
        else:
            create_args = {}
            for k, v in kwargs.items():
                if k in self.keys:
                    create_args[k] = v

            # Warn if keys of self.log_format are not set on write
            unset_keys = set(self.keys) - set(create_args.keys())
            if len(unset_keys):
                log.warning(f"The following log keys are unset: {unset_keys}")

            # Support enforcing all keys must be present. If log format class provides no default values
            rec = None
            try:
                rec = self.format(**create_args)  # type: ignore
            except TypeError as e:
                log.error(
                    f"Could not create log: {str(e.args)}", exc_info=True
                )

        self.write_log(rec)

    def write_log(self, rec: Any) -> None:
        """Write a message to the repoort

        Args:
            rec (self.format): record

        Raises:
            ValueError: If there is no record to write
        """
        if not rec:
            raise ValueError(
                f"Record must contain a dictionary to write, got '{rec}'"
            )

        if self.output_type == "csv":
            self.csv_writer.writerow(dataclasses.asdict(rec))
        else:
            if self.first_record:
                self.first_record = False
            else:
                self.file_cursor.write(",\n")
            json.dump(dataclasses.asdict(rec), self.file_cursor, indent=4)

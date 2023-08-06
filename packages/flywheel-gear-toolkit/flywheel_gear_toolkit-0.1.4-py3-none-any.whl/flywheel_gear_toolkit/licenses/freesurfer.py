"""Install Freesurfer license.txt file where algorithm expects it.
"""

from pathlib import Path
import shutil
import logging

log = logging.getLogger(__name__)


def install_freesurfer_license(context, fs_license_path):
    """Install the Freesurfer license file.

    The file is written at the provided path.  License text is found in one of
    3 ways and in this order:

    1) license.txt is provided as an input file,
    2) the text from license.txt is pasted into the "gear-FREESURFER_LICENSE"
       config, or
    3) the text from license.txt is pasted into a Flywheel project's "info"
       metadata.

    See `How to include a Freesurfer license file...
    <https://docs.flywheel.io/hc/en-us/articles/360013235453>`_

    Args:
        context (flywheel.gear_context.GearContext): The gear context with core
            functionality.
        fs_license_path (str): Path to where the license should be installed,
            $FREESURFER_HOME, usually "/opt/freesurfer/license.txt".

    Examples:
        >>> from .license.freesurfer import install_freesurfer_license
        >>> install_freesurfer_license(context, '/opt/freesurfer/license.txt')
    """

    log.debug("Looking for Freesurfer license")

    license_info = ""

    # 1) Check if the required FreeSurfer license file has been provided
    # as an input file.
    input_license = context.get_input_path("freesurfer_license")

    if input_license:  # just copy the file to the right place

        fs_path_only = Path(fs_license_path).parents[0]
        fs_file = Path(fs_license_path).name

        if fs_file != "license.txt":
            log.warning(
                "Freesurfer license file is usually license.txt, not " "%s",
                fs_license_path,
            )

        if not Path(fs_path_only).exists():
            Path(fs_path_only).mkdir(parents=True)
            log.warning(
                "Had to make freesurfer license path: %s", fs_license_path
            )

        shutil.copy(input_license, fs_license_path)

        license_info = "copied info file"
        log.info("Using FreeSurfer license in input file.")

    # 2) see if the license info was passed as a string argument
    elif context.config.get("gear-FREESURFER_LICENSE"):
        fs_arg = context.config["gear-FREESURFER_LICENSE"]
        license_info = "\n".join(fs_arg.split())

        log.info("Using FreeSurfer license in gear argument.")

    # 3) see if the license info is in the project's info
    else:

        fly = context.client
        destination_id = context.destination.get("id")
        project_id = fly.get_analysis(destination_id)["parents"]["project"]
        project = fly.get_project(project_id)

        if "FREESURFER_LICENSE" in project["info"]:
            space_separated_text = project["info"]["FREESURFER_LICENSE"]
            license_info = "\n".join(space_separated_text.split())

            log.info("Using FreeSurfer license in project info.")

    # If it was passed as a string or was found in info, license_info is
    # set so save the Freesurfer license as a file in the right place.
    # If the license was an input file, it was copied to the right place
    # above (case 1).
    if license_info == "copied info file":
        pass  # all is well

    elif license_info != "":

        head = Path(fs_license_path).parents[0]

        if not Path(head).exists():
            Path(head).mkdir(parents=True)
            log.debug("Created directory %s", head)

        with open(fs_license_path, "w") as flp:
            flp.write(license_info)
            log.debug("Wrote license %s", license_info)
            log.debug(" to license file %s", fs_license_path)

    else:
        msg = "Could not find FreeSurfer license anywhere"
        raise FileNotFoundError(f"{msg} ({fs_license_path}).")

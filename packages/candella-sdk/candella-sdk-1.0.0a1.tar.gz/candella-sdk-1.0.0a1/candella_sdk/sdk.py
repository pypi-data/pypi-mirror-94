"""The primary module for all SDK functions such as creating apps and services, validating manifests, etc."""
from enum import Enum
from cookiecutter.main import cookiecutter
import os
import json


class CandellaProjectType(Enum):
    """An enumeration of the different project types."""
    application = "app"
    core_service = "service"
    framework = "framework"
    unknown = "None"


__MANIFEST_VALID_KEYS = {
    CandellaProjectType.application: [
        "name", "productName", "id", "author", "version", "description", "permissions", "requisites", "license"
    ],
    CandellaProjectType.core_service: [
        "name", "id", "author", "version", "description", "permissions", "requisites", "license"
    ],
    CandellaProjectType.framework: [
        "name", "id", "author", "version", "description", "requisites", "license"
    ]
}

__MANIFEST_REQUIRED_KEYS = {
    CandellaProjectType.application: [
        "name", "id", "author", "version", "description", "permissions", "license"
    ],
    CandellaProjectType.core_service: [
        "name", "id", "author", "version", "description", "permissions", "requisites", "license"
    ],
    CandellaProjectType.framework: __MANIFEST_VALID_KEYS[CandellaProjectType.framework]
}


def __path_to_project_type(path: str):
    """Returns the project type based on the project's file extension."""
    if path.endswith(".aosapp"):
        return CandellaProjectType.application
    elif path.endswith(".aoscservice"):
        return CandellaProjectType.core_service
    elif path.endswith(".aosframework"):
        return CandellaProjectType.framework
    else:
        return CandellaProjectType.unknown


def create(project_type: CandellaProjectType):
    """Create a Candella project using a Cookiecutter template.

    Arguments:
        proj(str): The project type to create. Allowed: application, service, framework.
    """
    if project_type == CandellaProjectType.unknown:
        print("The specified project type is not valid.")
        return

    cookiecutter(
        f"https://github.com/UnscriptedVN/candella-{project_type.value}-template.git")


def validate(path: str):
    # Ensure the directory specified is a valid project.
    project_type = __path_to_project_type(path)
    if project_type == CandellaProjectType.unknown:
        return False, "unknown project type"

    # Ensure that the appropriate manifest file exists.
    if not os.path.isfile(os.path.join(path, "manifest.json")):
        return False, "missing manifest.json file"
    with open(os.path.join(path, "manifest.json"), 'r') as manifest_file:
        manifest = json.load(manifest_file)

    # TODO: This code is not really optimized. We're checking the manifest list twice for required keys
    # and for invalid keys, meaning that we have complexity of O(2n).

    # Ensure that the manifest doesn't contain any invalid keys.
    for key in manifest:
        if project_type == CandellaProjectType.application and \
                key not in __MANIFEST_VALID_KEYS[CandellaProjectType.application]:
            return False, f"invalid manifest key: {key}"
        elif project_type == CandellaProjectType.core_service and \
                key not in __MANIFEST_VALID_KEYS[CandellaProjectType.core_service]:
            return False, f"invalid manifest key: {key}"
        elif project_type == CandellaProjectType.framework and \
                key not in __MANIFEST_VALID_KEYS[CandellaProjectType.framework]:
            return False, f"invalid manifest key: {key}"

    # Likewise, check that the manifests have all of the required keys.
    if project_type == CandellaProjectType.application:
        for key in __MANIFEST_REQUIRED_KEYS[CandellaProjectType.application]:
            if key not in manifest:
                return False, f"missing required key: {key}"
    elif project_type == CandellaProjectType.core_service:
        for key in __MANIFEST_REQUIRED_KEYS[CandellaProjectType.core_service]:
            if key not in manifest:
                return False, f"missing required key: {key}"
    elif project_type == CandellaProjectType.framework:
        for key in __MANIFEST_REQUIRED_KEYS[CandellaProjectType.framework]:
            if key not in manifest:
                return False, f"missing required key: {key}"

    # Ensure that apps and core services have the iconset folder.
    if (project_type == CandellaProjectType.application or project_type == CandellaProjectType.core_service) and \
            not os.path.isdir(os.path.join(path, "Resources", "Iconset")):
        return False, "missing iconset folder"

    return True, ""

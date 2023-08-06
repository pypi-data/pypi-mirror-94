"""Version information for this package."""
### IMPORTS
### ============================================================================
## Standard Library

## Installed

## Application

### CONSTANTS
### ============================================================================
## Version Information - DO NOT EDIT
## -----------------------------------------------------------------------------
# These variables will be set during the build process. Do not attempt to edit.
PACKAGE_VERSION = "0.1.0"
BUILD_VERSION = "0.1.0.1613193646"
BUILD_GIT_HASH = "ebe7017747598971cd283772e1a66316026bc58b"
BUILD_GIT_HASH_SHORT = "ebe7017"
BUILD_GIT_BRANCH = "master"
BUILD_TIMESTAMP = 1613193646
BUILD_DATETIME = datetime.datetime.utcfromtimestamp(1613193646)

VERSION_VARS = vars()  # Don't have f-strings until py36

## Version Information Templates
## -----------------------------------------------------------------------------
# You can customise the templates used for version information here.
VERSION_INFO_TEMPLATE_SHORT = "{BUILD_VERSION}"
VERSION_INFO_TEMPLATE = "{PACKAGE_VERSION} ({BUILD_VERSION})"
VERSION_INFO_TEMPLATE_LONG = (
    "{PACKAGE_VERSION} ({BUILD_VERSION}) ({BUILD_GIT_BRANCH}@{BUILD_GIT_HASH_SHORT})"
)
VERSION_INFO_TEMPLATE_FULL = (
    "{PACKAGE_VERSION} ({BUILD_VERSION})\n"
    "{BUILD_GIT_BRANCH}@{BUILD_GIT_HASH}\n"
    "Built: {BUILD_DATETIME}"
)

### FUNCTIONS
### ============================================================================
def get_version_info_short() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE_SHORT.format(**VERSION_VARS)


def get_version_info() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE.format(**VERSION_VARS)


def get_version_info_long() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE_LONG.format(**VERSION_VARS)


def get_version_info_full() -> str:  # pylint: disable=missing-function-docstring
    return VERSION_INFO_TEMPLATE_FULL.format(**VERSION_VARS)

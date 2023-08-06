import sys

import os_xml_handler.xml_handler as xh
from os_android_app_automation.bp import _res as res
from os_android_app_version_changer import version_changer
from os_android_app_version_changer.objs.VersionProperties import VersionProperties
import fileinput


# will set the dependencies of the project to be as the user required
def set_dependencies(project_build_gradle, dependencies_nodes):
    dependencies_str = ''
    for dependency_node in dependencies_nodes:
        dependencies_str += xh.get_text_from_node(dependency_node)

    for line in fileinput.input(project_build_gradle, inplace=1):
        sys.stdout.write(line)
        if 'dependencies {' in line:
            sys.stdout.write(dependencies_str)
            sys.stdout.write('\n}')
            return


# will set the versions of the project to be as the user required
def set_versions(project_path, logger, version_name, version_code):
    version_name = _fix_version_value(logger, res.VERSION_NAME, version_name)
    version_code = _fix_version_value(logger, res.VERSION_CODE, version_code)
    version_properties = VersionProperties(version_code, version_name)
    version_changer.change_version(project_path, version_properties)


# will fix the version value to be as the VersionProperties require
def _fix_version_value(logger, version_type, version_value):
    if version_value is None:
        logger.info(f'{version_type} is None: keeping the same properties')
        return VersionProperties.KEEP_OLD_VERSION
    elif version_value is res.TAG_VERSION_RAISE:
        logger.info(f'Raising {version_type} in 1')
        return VersionProperties.RAISE_VERSION_BY_ONE
    return version_value

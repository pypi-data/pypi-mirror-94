# system
import os
import re
import fileinput
import sys

# project
from os_android_apk_builder.objs.VersionProperties import VersionProperties
from os_android_apk_builder.objs.KeyStoreProperties import KeyStoreProperties
from os_android_apk_builder.bp import _res

# os
from os_file_handler import file_handler as fh
import os_tools.string_utils as su


################################################################################
# this file includes all of the required actions to be used on                 #
# the build.gradle file, in order to prepare it for the apk/app bundle release #
################################################################################


# will check if needs to append all of the key store values in the build.gradle file
def check_if_release_enabled(path):
    build_gradle_file = os.path.join(path, 'app', 'build.gradle')
    release_command = "signingConfig signingConfigs.release"
    return not fh.is_line_exists_in_file(build_gradle_file, release_command)


# will prepare the build gradle file for the current release. This include (but not limited to) change the version code and name, setting the signinConfig, and more
def prepare_build_gradle_for_release(project_path, key_store_properties, version_properties, append_signin):
    build_gradle_file = os.path.join(project_path, 'app', 'build.gradle')
    version_code_set = False
    version_name_set = False
    on_android_par = False
    on_build_types_par = False
    added_signin = False

    for line in fileinput.input(build_gradle_file, inplace=1):
        # set the right version name or version code, if required
        if not version_code_set and version_properties.new_version_code != VersionProperties.KEEP_OLD_VERSION and _res.VERSION_CODE in line:
            line = change_version_props(line, version_properties.new_version_code, _res.VERSION_CODE)
            sys.stdout.write(line)
            version_code_set = True
            continue

        elif not version_name_set and version_properties.new_version_name != VersionProperties.KEEP_OLD_VERSION and _res.VERSION_NAME in line:
            line = change_version_props(line, version_properties.new_version_name, _res.VERSION_NAME)
            sys.stdout.write(line)
            version_name_set = True
            continue

        sys.stdout.write(line)

        if not append_signin:
            continue

        sanitized_line = su.str_to_words(line, ['{'])
        if sanitized_line == _res.PH_ANDROID:
            on_android_par = True

        # on android parenthesis (android {)
        if on_android_par:

            if not added_signin:
                sys.stdout.write(f'\n\t{_res.PH_GRADLE_LOG_SIGN_IN_START}')
                sys.stdout.write('\n\tsigningConfigs {')
                sys.stdout.write('\n\t\trelease {')
                sys.stdout.write('\n')
                append_signin_file_lines(key_store_properties)
                sys.stdout.write('\t\t}\n')
                sys.stdout.write('\t}\n')
                sys.stdout.write(f'\t{_res.PH_GRADLE_LOG_SIGN_IN_END}')
                sys.stdout.write('\n\n')

                added_signin = True
                continue

            if sanitized_line == _res.PH_BUILD_TYPES:
                on_build_types_par = True
                continue

            # on build types parenthesis (buildTypes {)
            if on_build_types_par:
                if sanitized_line == _res.PH_RELEASE:
                    sys.stdout.write(f'\t\t\t{_res.PH_GRADLE_LOG_SIGN_IN_RELEASE}')
                    continue


# will append the lines of the signin file, one by one, with the user sign in props
def append_signin_file_lines(key_store_properties: KeyStoreProperties):
    for key, val in key_store_properties.build_signin_dict().items():
        sys.stdout.write(f'\t\t\t{key} {val}\n')


# will set and get the current version of the project
def change_version_props(line, new_version, version_name):
    # set the right version name or version code, if required
    line_without_version = re.sub('[.0-9"+]', '', line).replace('\n', '').rstrip()

    if new_version != VersionProperties.KEEP_OLD_VERSION and version_name in line:

        # if raise version by one
        if new_version == VersionProperties.RAISE_VERSION_BY_ONE:
            curr_version = re.sub('[a-zA-Z" +]', '', line).replace('\n', '')
            if '.' not in curr_version:
                curr_version = int(curr_version) + 1
            else:
                version = curr_version.split('.')
                version[-1] = str(int(version[-1]) + 1)
                curr_version = '.'.join(version)
            if version_name == _res.VERSION_NAME:
                curr_version = f'"{curr_version}"'
            return f'{line_without_version} {curr_version}\n'
        else:
            if version_name == _res.VERSION_NAME:
                new_version = f'"{new_version}"'
            return f'{line_without_version} {new_version}\n'


# will obtain the current version code from the project
def obtain_version_code(project_path):
    build_gradle_file = _res.get_build_gradle_file(project_path)
    line = fh.get_line_from_file(build_gradle_file, _res.VERSION_CODE)
    last_space_idx = line.rfind(" ")
    new_line = line.rfind("\n")
    version_code = line[last_space_idx + 1:new_line]
    return version_code


# will remove the user signed in params from the gradle, upon process end
def remove_sign_in_config_from_gradle(project_path):
    build_gradle_file = _res.get_build_gradle_file(project_path)
    fh.remove_lines_from_file(build_gradle_file, [_res.PH_GRADLE_LOG_SIGNATURE], _res.PH_GRADLE_LOG_SIGN_IN_START, _res.PH_GRADLE_LOG_SIGN_IN_END)

import os

from os_android_apk_builder.bp import _general_utils
import os_tools.logger_handler as lh
from os_android_apk_builder.objs.KeyStoreProperties import KeyStoreProperties
from os_android_app_version_changer.objs.VersionProperties import VersionProperties
from os_file_handler import file_handler as fh
from os_android_apk_builder.bp import _build_gradle_utils
from os_android_apk_builder.bp import _res


############################################################
# This module aim is to build an Android apk/App Bundle.   #
# the name of the released apk will be the versionName.apk #
############################################################


def build_apk(project_path,
              apk_dst_dir_path,
              key_store_properties: KeyStoreProperties,
              version_properties: VersionProperties,
              gradle_path=None,
              remove_older_apks_from_output_dir=False):
    """
    Will create an Android APK (.apk) file.

    Args:
        project_path: the path to your android app's project
        apk_dst_dir_path: the path to the directory in which the made apk will be stored. The name of the released apk will be the versionName.apk
        key_store_properties: an instance which holds the properties of your KeyStore
        version_properties: an instance which holds the properties of your published version
        gradle_path: the path to your gradle file (if left blank, will use the gradle wrapper in the project).
        you can also use the gradle on your system by setting 'gradle'
        remove_older_apks_from_output_dir: set to true if you want to clear the output dir from any old .apk files.
        This will fire only if a new .apk will be made
    """
    _build(project_path, apk_dst_dir_path, key_store_properties, version_properties, gradle_path, _res.APK, remove_older_apks_from_output_dir)


def build_app_bundle(project_path,
                     app_bundle_dst_dir_path,
                     key_store_properties: KeyStoreProperties,
                     version_properties: VersionProperties,
                     gradle_path=None,
                     remove_older_app_bundles_from_output_dir=False):
    """
    Will create an Android AppBundle (.aab) file.

    Args:
        project_path: the path to your android app's project
        app_bundle_dst_dir_path: the path to the directory in which the made .aab will be stored. The name of the released apk will be the versionName.aab
        key_store_properties: an instance which holds the properties of your KeyStore
        version_properties: an instance which holds the properties of your published version
        gradle_path: the path to your gradle file (if left blank, will use the gradle wrapper in the project).
        you can also use the gradle on your system by setting 'gradle'
        remove_older_app_bundles_from_output_dir: set to true if you want to clear the output dir from any old .aab files.
        This will fire only if a new .aab will be made
    """
    _build(project_path, app_bundle_dst_dir_path, key_store_properties, version_properties, gradle_path, _res.APP_BUNDLE, remove_older_app_bundles_from_output_dir)


def _build(project_path, output_dir, key_store_properties: KeyStoreProperties, version_properties: VersionProperties, gradle_path, binary_type, remove_older_binaries):
    logger = lh.Logger(name='[APK Builder]')  # build the logger

    # will prepare any resources according to the binary type
    if binary_type == _res.APK:
        release_command = _res.COMMAND_APK_GRADLE_RELEASE
        binary_release_path = _res.get_apk_output_path(project_path)
        binary_ext = _res.EXT_APK
    elif binary_type == _res.APP_BUNDLE:
        release_command = _res.COMMAND_APP_BUNDLE_GRADLE_RELEASE
        binary_release_path = _res.get_app_bundle_output_path(project_path)
        binary_ext = _res.EXT_APP_BUNDLE
    else:
        raise NotImplementedError(f"Unrecognized '{binary_type}' binary type")

    # check if 'signingConfig signingConfigs.release' exists in the build.gradle file
    is_release_enabled = _build_gradle_utils.check_if_release_enabled(project_path)

    if not is_release_enabled:
        logger.warning('*** NOTICE: build.gradle file has the line: "signingConfig signingConfigs.release". If you want to use KeyStoreProperties, remove this line from your build.gradle')

    logger.info('Preparing build.gradle file for automated release...')
    _build_gradle_utils.prepare_build_gradle_for_release(project_path, key_store_properties, version_properties, is_release_enabled)

    # clear latest binary file
    logger.info(f'Clearing latest {binary_ext} file from project...')
    fh.remove_file(binary_release_path)

    # create the binary
    logger.info(f'Building the {binary_type}...')
    _general_utils.release_binary(release_command, project_path, gradle_path)

    # if the apk creation failed, throw an exception
    if not fh.is_file_exists(binary_release_path):
        raise Exception(f"ERROR: Failed to create {binary_type} file")

    if remove_older_binaries:
        logger.info(f'Gradle finished! removing older {binary_ext} files from {output_dir} dir...')
        # remove previous apks from the directory
        fh.remove_all_files_with_extension(binary_release_path, binary_ext)

    logger.info(f'Copying the new {binary_ext} file...')
    # copy the binary to the user desired location (with the file name as the version code)

    # obtain the version code
    version_code = _build_gradle_utils.obtain_version_code(project_path)
    binary_dst_path = os.path.join(output_dir, f'{version_code}{binary_ext}')
    fh.copy_file(binary_release_path, binary_dst_path)

    logger.info('Sanitizing build.gradle file...')
    # revert the build.gradle file to it's previous form
    _build_gradle_utils.remove_sign_in_config_from_gradle(project_path)

    logger.info(f'{binary_type} file built successfully in:\n {binary_dst_path}')

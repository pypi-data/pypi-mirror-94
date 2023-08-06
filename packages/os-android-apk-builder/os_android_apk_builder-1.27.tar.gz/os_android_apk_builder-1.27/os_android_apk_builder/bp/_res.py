import os

# outputs
OUTPUTS_PATH = os.path.join('app', 'build', 'outputs')
REL_PATH_APP_BUNDLE_RELEASE = os.path.join(OUTPUTS_PATH, 'bundle', 'release', 'app-release.aab')
REL_PATH_APK_RELEASE = os.path.join(OUTPUTS_PATH, 'apk', 'release', 'app-release.apk')

# ext
EXT_APK = '.apk'
EXT_APP_BUNDLE = '.aab'

# version
VERSION_CODE = "versionCode"
# cmd commands
COMMAND_APK_GRADLE_RELEASE = "assembleRelease"
COMMAND_APP_BUNDLE_GRADLE_RELEASE = ":app:bundle"
RELEASE_COMMAND = "signingConfig signingConfigs.release"

# build.gradle place holders
PH_ANDROID = ['android', '{']
PH_BUILD_TYPES = ['buildTypes', '{']
PH_RELEASE = ['release', '{']
PH_GRADLE_LOG_SIGNATURE = 'apk_builder'
PH_GRADLE_LOG_SIGN_IN_START = f'// {PH_GRADLE_LOG_SIGNATURE} -> auto generated sign in config start'
PH_GRADLE_LOG_SIGN_IN_END = f'// {PH_GRADLE_LOG_SIGNATURE} -> auto generated sign in config end'
PH_GRADLE_LOG_SIGN_IN_RELEASE = f'signingConfig signingConfigs.release  // {PH_GRADLE_LOG_SIGNATURE} -> auto generated sign in config release\n'

# signin file
KEY_STORE_FILE_PATH = 'storeFile'
KEY_STORE_PASSWORD = 'storePassword'
KEY_KEY_ALIAS = 'keyAlias'
KEY_KEY_PASSWORD = 'keyPassword'
KEY_V1_SIGNING_ENABLED = 'v1SigningEnabled'
KEY_V2_SIGNING_ENABLED = 'v2SigningEnabled'

APK = 'apk'
APP_BUNDLE = 'app bundle'


# will return the current build.gradle file
def get_build_gradle_file(project_path):
    return os.path.join(project_path, 'app', 'build.gradle')


# will return the current output of the apk file
def get_apk_output_path(project_path):
    return os.path.join(project_path, REL_PATH_APK_RELEASE)


# will return the required output of the app bundle file
def get_app_bundle_output_path(project_path):
    return os.path.join(project_path, REL_PATH_APP_BUNDLE_RELEASE)

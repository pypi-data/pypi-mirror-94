# system
import os

##########################################
# just a boilerPlate for the apk release #
##########################################


# will run the command which will create the binary (apk/app bundle)
def release_binary(release_command, project_path, gradle_path):

    # if the gradle path is None, we will use the project's gradle wrapper
    if gradle_path is None:
        gradle_path = os.path.join(project_path, 'gradlew')

    cd_command = f'cd {project_path}'
    gradle_command = f'{gradle_path} {release_command}'
    full_command = f'{cd_command} && {gradle_command}'
    os.system(full_command)
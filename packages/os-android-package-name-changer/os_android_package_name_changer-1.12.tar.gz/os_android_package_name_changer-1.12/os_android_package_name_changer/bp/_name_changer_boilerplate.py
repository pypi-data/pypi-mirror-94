import os
import shutil
import os_file_handler.file_handler as fh
from os_file_stream_handler import file_stream_handler as fsh


##########################################
# just a bp file for the name_changer.py #
##########################################


def change_package_name(path_to_project, old_package_name, new_package_name):
    # run on all of the files and replace all occurrences of old_package_name with new_package_name
    for dname, dirs, files in os.walk(path_to_project):
        for fname in files:
            fpath = os.path.join(dname, fname)
            try:
                with open(fpath) as f:
                    s = f.read()

                s = s.replace(old_package_name, new_package_name)
                with open(fpath, "w") as f:
                    f.write(s)
            except:
                pass

    # clear caches
    gradle_path = path_to_project + "/.gradle"
    if os.path.exists(gradle_path):
        shutil.rmtree(gradle_path)


def check_write_permission(path_to_project):
    # check if necessary files are writable
    for dname, dirs, files in os.walk(path_to_project):
        if '.git' in dname:
            continue
        for fname in files:
            fpath = os.path.join(dname, fname)
            if not fh.is_file_write_permission_granted(fpath):
                raise Exception("ERROR: To change the package name, you need to allow write permission to: " + fpath)


def change_inner_folders_names(project_path, old_package_name, new_package_name):
    # get the dirs names of inner folders inside the main and tests
    new_package_name = new_package_name.split(".")
    first_new_word = new_package_name[1]
    second_new_word = new_package_name[2]

    old_package_name = old_package_name.split(".")
    first_old_word = old_package_name[1]
    second_old_word = old_package_name[2]

    # change the two inner folders in the main dir
    main_com_dir = os.path.join(project_path, 'app', 'src', 'main', 'java', 'com')
    if fh.is_dir_exists(os.path.join(main_com_dir, first_old_word, second_old_word)):
        shutil.move(os.path.join(main_com_dir, first_old_word, second_old_word), os.path.join(main_com_dir, first_old_word, second_new_word))
        shutil.move(os.path.join(main_com_dir, first_old_word), os.path.join(main_com_dir, first_new_word))

    # change the two inner folders in the test dir
    test_com_dir = os.path.join(project_path, 'app', 'src', 'test', 'java', 'com')
    if fh.is_dir_exists(os.path.join(test_com_dir, first_old_word, second_old_word)):
        shutil.move(os.path.join(test_com_dir, first_old_word, second_old_word), os.path.join(test_com_dir, first_old_word, second_new_word))
        shutil.move(os.path.join(test_com_dir, first_old_word), os.path.join(test_com_dir, first_new_word))

    # change the two inner folders in the android test dir
    test_android_com_dir = os.path.join(project_path, 'app', 'src', 'androidTest', 'java', 'com')
    if fh.is_dir_exists(os.path.join(test_android_com_dir, first_old_word, second_old_word)):
        shutil.move(os.path.join(test_android_com_dir, first_old_word, second_old_word), os.path.join(test_android_com_dir, first_old_word, second_new_word))
        shutil.move(os.path.join(test_android_com_dir, first_old_word), os.path.join(test_android_com_dir, first_new_word))


def change_settings_gradle_file(project_path, new_package_name):
    settings_gradle = os.path.join(project_path, 'settings.gradle')
    package_name_last_segment = new_package_name[str(new_package_name).rfind('.')+1:]
    new_expression = f'rootProject.name = "{package_name_last_segment}"'
    fsh.replace_text_in_file(settings_gradle, settings_gradle, 'rootProject.name', new_expression, replace_whole_line=True)

import os
import sys
import subprocess


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

            windows_executable = os.path.join(path, '{}.exe'.format(program))
            if is_exe(windows_executable):
                return windows_executable
    return None


def convert_terraform_plan_to_json(terraform_plan_file, terraform_executable=None):
    print('. Converting terraform plan file.')
    if terraform_executable is None:
        terraform_executable = which('terraform')
    else:
        print('Using {} as terraform executable.'.format(terraform_executable))

    if terraform_executable is None:
        sys.stderr.write('ERROR: Could not find "terraform" executable in PATH. Please either use "-t" parameter '
                         'or add terraform executable to your PATH.\n')
        sys.exit(1)

    path = os.path.dirname(terraform_plan_file)
    cwd = os.getcwd()
    os.chdir(path)

    try:
        with open('{}.json'.format(terraform_plan_file), 'w', encoding='utf-8') as FP_plan_file:
            terraform = subprocess.run([terraform_executable, 'show', '-json', terraform_plan_file],
                                       universal_newlines=True,
                                       stdout=FP_plan_file,
                                       stderr=subprocess.PIPE)
    except FileNotFoundError as err:
        sys.stderr.write('ERROR: {} does not exist. Please give correct executable for "terraform".\n'.format(terraform_executable))
        sys.stderr.write('       {}\n'.format(str(err)))
        sys.exit(1)
    except PermissionError  as err:
        sys.stderr.write('ERROR: {} is not executable. Please give correct executable for "terraform".\n'.format(terraform_executable))
        sys.stderr.write('       {}\n'.format(str(err)))
        sys.exit(1)
    except OSError as err:
        sys.stderr.write('ERROR: {} does not look like terraform. Please give correct executable for "terraform".\n'.format(terraform_executable))
        sys.stderr.write('       {}\n'.format(str(err)))
        sys.exit(1)

    os.chdir(cwd)

    if terraform.returncode == 0:
        return '{}.json'.format(terraform_plan_file)

    sys.stderr.write('ERROR: Failed to convert terraform plan file to JSON format via terraform. Here is the error :\n')
    print(terraform.stdout)
    print(terraform.stderr)

    if 'Could not satisfy plugin requirements' in terraform.stderr:
        print('Hint: You can avoid this problem by converting your plan file to a JSON file via running;\n '
              '\n    # terraform show -json {} > {}.json'
              '\n\n                          OR'
              '\n    # terraform init'
              '\n\n in {} directory and then pass (with -p) {}.json to terraform-compliance'.format(terraform_plan_file,
                                                                                                    terraform_plan_file,
                                                                                                    path,
                                                                                                    terraform_plan_file))

    sys.exit(1)

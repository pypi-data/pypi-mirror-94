import subprocess

def run_commands(commands: str) -> str:
    process = subprocess.Popen(
                        commands,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        shell=True)

    stdout, stderr = process.communicate()

    if len(stdout) > 0:
        stdout = stdout.decode('utf-8')

    if len(stderr) > 0:
        stderr = stderr.decode('utf-8')

    command_output_list = []

    if len(stdout) > 0:
        command_output_list.append(stdout)

    if len(stderr) > 0:
        command_output_list.append(stderr)

    command_output = '\n'.join(command_output_list)

    return command_output

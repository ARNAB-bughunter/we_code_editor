import subprocess


MAX_TIME_OUT = 120

def update_file(code):
    with open("src/service/user_code.py", "w") as file:
        file.write(code)

def executer(msg_id):
    # Execute the command and capture the container ID
    run_command = f"docker run -d --rm --name my-running-script-{msg_id} -v $PWD:/myapp -w /myapp  python:3.12-alpine python src/service/user_code.py"
    result = subprocess.run(run_command, shell=True, capture_output=True, text=True)

    container_id = result.stdout.strip()
    
    # Wait for the container to finish and get its logs (output)
    log_command = f"docker logs -f {container_id}"
    try:
        logs = subprocess.run(log_command, shell=True, capture_output=True, text=True,timeout=MAX_TIME_OUT) # run container only for MAX_TIME_OUT second then kill
    except Exception as e:
        remove_commmand = f"docker rm -f {container_id}"
        subprocess.run(remove_commmand, shell=True, capture_output=True, text=True)
        return "ERROR", container_id
    return logs.stdout, container_id


    # command = ['docker', 'run', '-it', '--rm', '--name', 'my-running-script',
    #            '-v', '$PWD:/myapp:Z', '-u', '$(id -u):$(id -g)', '-w', '/myapp',
    #            'python:3.7-alpine', 'python', 'user_code.py']
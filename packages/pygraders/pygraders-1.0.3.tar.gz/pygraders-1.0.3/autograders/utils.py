import os
import re
import time
import boto3
import signal
import socket
import paramiko
import threading
from subprocess import PIPE
from subprocess import Popen
from datetime import datetime


def get_timestamp():
    '''Gets an UTC timestamp

    Returns
    -------
    datetime
        A datetime object filled with the current UTC date and time
    '''
    return datetime.utcnow()


def read_file(filename, cwd='.', encoding='utf-8'):
    '''Reads a file

    Parameters
    ----------
    filename: str
        Filename to read
    cwd: str
        Current working directory
    encoding: str
        File encoding

    Returns
    -------
    str
        All the text from the file
    '''
    f = open(os.path.join(cwd, filename), 'r', encoding=encoding)
    text = f.read()
    f.close()
    return text.strip()


# parses a form
def parse_form(filename, cwd='.'):
    '''Parses a form

    Parameters
    ----------
    filename: str
        Form filename
    cwd: str
        Current working directory

    Returns
    -------
    dic
        A dictionary with the answers
    '''
    try:
        f = open(os.path.join(cwd, filename), 'r', encoding='utf-8')
        p = re.compile(r'^[0-9]+?( )*?:[a-zA-Z0-9, ]+?$')
        lookup = {}
        for line in f:
            line = line.strip()
            line = re.sub(r'( |\t)+', ' ', line)
            line = re.sub(r'( |\t)*,( |\t)*', ',', line)
            if p.search(line) is not None:
                key, value = line.split(':')
                lookup[key.strip()] = value.strip()
        return lookup
    except Exception:
        return {}


def execute(cmd=[], cwd='.', shell=False, input=None, encoding='utf-8', timeout=5):
    '''Executes a command

    Parameters
    ----------
    cmd: list or str
        Command to execute
    cwd: str
        Current working directory
    shell: bool
        If shell is True, the specified command will be executed through the shell
    input: str or None
        Input to write in stdin
    encoding: str
        Input encoding
    timeout: int
        Execution timeout in seconds

    Returns
    -------
    ExecuteResult
        Execution result
    '''
    class ExecuteResult:
        def __init__(self):
            self.stdout = ''
            self.stderr = ''
            self.code = 0
            self.timeout = False

        def __str__(self):
            return self.stdout

    class Execute(threading.Thread):

        def __init__(self, cmd, shell, input, encoding, cwd='.'):
            super().__init__()
            self._stop_event = threading.Event()
            self.process = Popen(cmd, shell=shell, cwd=cwd, stdout=PIPE, stdin=PIPE, stderr=PIPE, preexec_fn=os.setsid)
            if input is not None and isinstance(input, str):
                self.process.stdin.write((input + os.linesep).encode(encoding))
                self.process.stdin.flush()
            self.result = ExecuteResult()

        def stop(self):
            self._stop_event.set()

        def run(self):
            while not self._stop_event.is_set():
                if self.process.poll() is not None:
                    self.result.stdout = self.process.stdout.read().decode().rstrip()
                    self.result.stderr = self.process.stderr.read().decode().rstrip()
                    self.result.code = self.process.returncode
                    self.result.timeout = False
                    break

            if self.result.timeout:
                self.result.timeout = True
                os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)

    t = Execute(cmd, shell, input, encoding, cwd=cwd)
    t.start()
    t.join(timeout=timeout)
    t.stop()
    return t.result


def make(target='', timeout=5):
    '''Executes a command

    Parameters
    ----------
    target: str
        Makefile target name
    timeout: int
        Execution timeout in seconds

    Returns
    -------
    ExecuteResult
        Execution result
    '''
    return execute(cmd=['make', target], timeout=timeout)


class EC2Instance:
    '''AWS EC2 Instance Task'''

    def __init__(self, name, itype, ami, sg, key, username='ubuntu', cwd='.', retries=3):
        '''
        Parameters
        ----------
        name: str
            Instance name
        itype: str
            Instance type (e.g t2.micro)
        ami: str
            AMI id (e.g ami-0bdb749fab1313b6a)
        sg: str
            Security group id (e.g sg-00b6ec171be0d43f7)
        key: str
            Connection private key (e.g autograders.pem)
        username: str (default: ubuntu)
            Instance username (e.g ubuntu)
        cwd: str
            Current working directory
        retries: int (default: 3)
            Number of times to retry connection
        '''
        ec2 = boto3.resource('ec2')
        self.instance = ec2.create_instances(
            ImageId=ami,
            MaxCount=1,
            MinCount=1,
            InstanceType=itype,
            SecurityGroupIds=[sg],
            KeyName=key.rstrip('.pem'),
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': name
                        },
                    ]
                },
            ],
        )[0]
        self.instance.wait_until_running()
        self.instance.reload()
        self.instance.wait_until_running()
        self.ipv4 = self.instance.public_ip_address

        # wait 60 seconds to connect
        time.sleep(60)

        # connection retries
        for i in range(1, retries + 1):
            try:
                pkey = paramiko.RSAKey.from_private_key_file(os.path.join(cwd, key))
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(hostname=self.ipv4, username=username, pkey=pkey)
                self.client = client
                # wait 30 seconds to retry
                time.sleep(30)
            except Exception as e:
                if i == retries:
                    self.instance.terminate()
                    raise e

    def execute(self, cmd=[], timeout=30):
        '''Executes command inside AWS EC2 instance

        Parameters
        ----------
        cmd: list
            Command to execute
        timeout: int
            Timeout in seconds

        Returns
        -------
        tuple
            tuple with stdout and stderr
        '''
        tout = False
        stdout = ''
        stderr = ''
        try:
            _, stdout, stderr = self.client.exec_command(' '.join(cmd), timeout=timeout)
            stdout = stdout.read().decode()
            stderr = stderr.read().decode()
        except (paramiko.buffered_pipe.PipeTimeout, socket.timeout):
            tout = True
            if isinstance(stdout, paramiko.channel.ChannelFile):
                stdout = stdout.read().decode()
            if isinstance(stderr, paramiko.channel.ChannelFile):
                stderr = stderr.read().decode()
        return (tout, stdout, stderr)

    def terminate(self):
        '''Terminates AWS EC2 instance

        Returns
        -------
        None
        '''
        self.client.close()
        self.instance.terminate()

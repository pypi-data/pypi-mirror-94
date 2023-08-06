import os
import sys
import json
import logging
from pathlib import Path
import docker
import traceback
import logging
import signal
from distutils.dir_util import copy_tree
from future.moves import subprocess

logger=logging.getLogger('mldock')


def train_model(working_dir, docker_tag, image_name, entrypoint, cmd, env=None):
    """
    Trains ML model(s) locally
    :param working_dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """
    process_env = None
    if env is not None:
        process_env = os.environ.copy()
        process_env.update(env)

    client = docker.from_env()

    try:
        container = client.containers.run(
            image="{image}:{tag}".format(image=image_name, tag=docker_tag),
            entrypoint=entrypoint,
            command=cmd,
            environment=process_env,
            remove=True,
            tty=True,
            volumes={
                '{test_path}/config'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/config', 'mode': 'rw'},
                '{test_path}/data'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/data', 'mode': 'rw'},
                '{test_path}/model'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/model', 'mode': 'rw'},
                '{test_path}/output'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/output', 'mode': 'rw'}
            },
            auto_remove=True,
            detach=True,
            stream=True
        )
        logs = container.logs(follow=True).decode('utf-8')

        logger.info(logs)
    except (KeyboardInterrupt, SystemExit) as exception:
        logger.error(exception)
        container.kill()
    except (docker.errors.APIError, docker.errors.ContainerError, docker.errors.ImageNotFound) as exception:
        logger.error(exception)
    except Exception as exception:
        logger.error(exception)

def deploy_model(working_dir, docker_tag, image_name, entrypoint, cmd, port=8080, env={}):
    """
    Deploys ML models(s) locally
    :param working_dir: [str], source root directory
    :param docker_tag: [str], the Docker tag for the image
    :param image_name: [str], The name of the Docker image
    """

    process_env = os.environ.copy()
    if isinstance(env, dict) & len(env) > 0:
        process_env.update(env)
    client = docker.from_env()

    try:
        container = client.containers.run(
            image="{image}:{tag}".format(image=image_name, tag=docker_tag),
            entrypoint=entrypoint,
            command=cmd,
            environment=process_env,
            ports={8080: port},
            remove=True,
            tty=True,
            volumes={
                '{test_path}/config'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/config', 'mode': 'rw'},
                '{test_path}/data'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/input/data', 'mode': 'rw'},
                '{test_path}/model'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/model', 'mode': 'rw'},
                '{test_path}/output'.format(test_path=os.path.abspath(working_dir)): {'bind': '/opt/ml/output', 'mode': 'rw'}
            },
            auto_remove=True,
            detach=True,
            stream=True
        )
        logs = container.logs(follow=True).decode('utf-8')

        logger.info(logs)
    except (KeyboardInterrupt, SystemExit) as exception:
        logger.error(exception)
        container.kill()
    except (docker.errors.APIError, docker.errors.ContainerError, docker.errors.ImageNotFound) as exception:
        logger.info(exception)
        logger.error(exception)
    except Exception as exception:
        logger.error(exception)

def pretty_build_logs(line: dict):
    error = line.get('error', None)
    errorDetail = line.get('errorDetail', None)
    if error is not None:
        logger.error('{}\n{}'.format(error, errorDetail))
    
    stream = line.get('stream','')

    if ('Step' in stream) & (':' in stream):
        logger.info(stream)
    else:
        logger.debug(stream)

def docker_build(
    image_name: str,
    dockerfile_path: str,
    module_path: str,
    target_dir_name: str,
    requirements_file_path: str,
    no_cache: bool
):
    """Runs the build executable from script path, passing a set of arguments in a command line subprocess.

    Args:
        script_path (str): relative path to script when run on root
        base_path (str):
        image_name (str):
        dockerfile_path (str):
        module_path (str):
        target_dir_name (str):
        requirements_file_path (str):
    """
    logger.info("\nStarting build...\n")
    try:
        cli = docker.APIClient(
            base_url=os.environ.get('DOCKER_HOST', 'tcp://127.0.0.1:2375')
        )
        short_log = []

        logs = cli.build(
            tag=image_name,
            path='.',
            dockerfile=os.path.join(dockerfile_path, 'Dockerfile'),
            buildargs={
                'module_path': module_path,
                'target_dir_name': target_dir_name,
                'requirements_file_path': requirements_file_path
            },
            quiet=False,
            nocache=no_cache,
            rm=True,
            decode=True
        )

        for line in logs:
            pretty_build_logs(line=line)
        logger.info("\nBuild Complete! ヽ(´▽`)/")
    except (KeyboardInterrupt, SystemExit) as exception:
        logger.error(exception)
        # container.kill()
    except (docker.errors.APIError, docker.errors.ContainerError, docker.errors.ImageNotFound) as exception:
        logger.info(exception)
        logger.error(exception)
    except Exception as exception:
        logger.error(exception)

def _rename_file(base_path, current_filename, new_filename):
    """renames filename for a given base_path, saving the file in the same base_path

    Args:
        base_path ([type]): directory path containing file to rename
        current_filename ([type]): current name of the file to rename
        new_filename ([type]): new name for the renamed file
    """
    Path(base_path, current_filename).rename(Path(base_path, new_filename))

def _create_empty_file(base_path, filename):
    """renames filename for a given base_path, saving the file in the same base_path

    Args:
        base_path ([type]): directory path containing file to rename
        current_filename ([type]): current name of the file to rename
        new_filename ([type]): new name for the renamed file
    """
    Path(base_path, filename).touch(exist_ok=True)

def _copy_boilerplate_to_dst(src: str, dst: str):
    """[summary]

    Args:
        src (str): [description]
        dst (str): [description]
    """
    source_path = str(Path(src).absolute())
    destination_path = str(Path(dst).absolute())
    copy_tree(source_path, destination_path)


def run_predict(script_path: str, host: str, payload: str, content_type: str):
    """Runs the predict shell script and passes the arguments as expected by the script.

    Args:
        script_path (str): relative path to script when run on root
        host (str): http/https host uri
        payload (str): relative path to payload file when run on root
        content_type (str): content type for request
    """
    logger.info("\nRunning Prediction...\n") 

    try:
        if content_type == 'application/json':
            result = subprocess.run([
                    script_path,
                    host,
                    payload,
                    content_type
                ],
                stdout=subprocess.PIPE
            )
            decoded_stdout = json.loads(result.stdout.decode())
            pretty_output = json.dumps(decoded_stdout, indent=4, separators=(',', ': '), sort_keys=True)
        elif content_type == 'text/csv':
            result = subprocess.run([
                    script_path,
                    host,
                    payload,
                    content_type
                ],
                stdout=subprocess.PIPE
            )
            pretty_output = result.stdout.decode()
        else:
            raise Exception('Only Supports application/json or text/csv')

        logger.info(pretty_output)
        logger.info("\nPrediction Complete! ヽ(´▽`)/")
        return pretty_output

    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

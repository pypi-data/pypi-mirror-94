import os
import sys
import json
import logging
import click
from pathlib import Path
from future.moves import subprocess

from mldock.config.config_manager import \
    ResourceConfigManager, MLDockConfigManager, PackageConfigManager, \
        HyperparameterConfigManager, InputDataConfigManager
from mldock.api.local import \
    run_predict, _copy_boilerplate_to_dst, docker_build, \
        _rename_file

from mldock.api.local import \
    train_model, deploy_model

click.disable_unicode_literals_warning = True
logger=logging.getLogger('mldock')

def _format_key_as_mldock_env_var(key, prefix='MLDOCK'):
    """
        Formats key as mldock env variable.
        Replace '\s' and '-', append mldock prefix
        and lastly transforms to uppercase
    """
    if prefix is not None:
        key = "{}_{}".format(prefix, key)
    key = key.replace(" ", "_").replace("-", "_")
    key = key.upper()
    return key

def _format_dictionary_as_env_vars(obj: dict):

    return {
        _format_key_as_mldock_env_var(_key): json.dumps(_value)
        for _key,_value in obj.items()
    }

@click.group()
def local():
    """
    Commands for local operations: train and deploy
    """
    pass

@click.command()
@click.option('--dir', help='Set the working directory for your mldock container.', required=True)
@click.option('--no-cache', help='builds container from scratch', is_flag=True)
@click.pass_obj
def build(obj, dir, no_cache):
    """build image using docker

    Args:
        dir (str): directory containing model assets
    """
    helper_library_path = obj['helper_library_path']
    try:
        mldock_manager = MLDockConfigManager(
            filepath=os.path.join(dir, ".mldock.json")
        )
        # get mldock_module_dir name
        mldock_config = mldock_manager.get_config()
        image_name = mldock_config.get("image_name", None)
        container_dir = mldock_config.get("container_dir", None)
        module_path = os.path.join(
            dir,
            mldock_config.get("mldock_module_dir", "src"),
        )
        dockerfile_path = os.path.join(
            dir,
            mldock_config.get("mldock_module_dir", "src"),
            container_dir
        )
        requirements_file_path = os.path.join(
            dir,
            mldock_config.get("requirements.txt", "requirements.txt")
        )
        if image_name is None:
            raise Exception("\nimage_name cannot be None")
        elif image_name.endswith(":latest"):
            raise Exception("\nImage version is not supported at this point. Please remove :latest versioning")
        else:
            docker_build(
                image_name=image_name,
                dockerfile_path=dockerfile_path,
                module_path=module_path,
                target_dir_name=mldock_config.get("mldock_module_dir", "src"),
                requirements_file_path=requirements_file_path,
                no_cache=no_cache
            )
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

@click.command()
@click.option('--payload', default=None, help='path to payload file', required=True)
@click.option('--content-type', help='format of payload', type=click.Choice(['json', 'csv'], case_sensitive=False))
@click.option('--host', help='host url at which model is served', type=str, default='http://127.0.0.1:8080')
@click.pass_obj
def predict(obj, payload, content_type, host):
    """
    Command to run curl predict against an host served on localhost:8080
    """
    helper_library_path = obj['helper_library_path']
    try:
        if payload is None:
            logger.info("\nPayload cannot be None")
        else:
            if content_type == "csv":
                content_type = 'text/csv'
                _ = run_predict(
                    script_path=os.path.join(helper_library_path,'api/predict_csv.sh'),
                    host=host,
                    payload=payload,
                    content_type=content_type
                )
            elif content_type == 'json':
                content_type = 'application/json'
                _ = run_predict(
                    script_path=os.path.join(helper_library_path,'api/predict_json.sh'),
                    host=host,
                    payload=payload,
                    content_type=content_type
                )
            else:
                raise TypeError("content-type of payload no supported. Only csv and json are supported at the moment")
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

@click.command()
@click.option('--dir', help='Set the working directory for your mldock container.', required=True)
@click.option('--tag', help='docker tag', type=str, default='latest')
@click.option('--stage', default='dev', help='environment to stage.', required=True)
@click.pass_obj
def train(obj, dir, tag, stage):
    """
    Command to train ML model(s) locally
    """
    mldock_manager = MLDockConfigManager(
        filepath=os.path.join(dir, ".mldock.json")
    )
    # get mldock_module_path name
    mldock_config = mldock_manager.get_config()
    module_path = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src"),
    )
    image_name = mldock_config.get("image_name", None)
    platform = mldock_config.get("platform", None)
    container_dir = mldock_config.get("container_dir", None)
    helper_library_path = obj['helper_library_path']
    hyperparameters_env_var = _format_dictionary_as_env_vars(
        {'hyperparameters': mldock_config.get('hyperparameters', {})}
    )
    project_env_vars = _format_dictionary_as_env_vars(mldock_config.get('environment', {}))
    env_vars={
        'stage': stage,
        **hyperparameters_env_var,
        **project_env_vars
    }
    try:
        if platform == "sagemaker":
            train_model(
                working_dir=dir,
                docker_tag=tag,
                image_name=image_name,
                entrypoint="container/executor.sh",
                cmd="train",
                env=env_vars
            )
        elif platform == "sagemakerv2":
            train_model(
                working_dir=dir,
                docker_tag=tag,
                image_name=image_name,
                entrypoint="src/container/executor.sh",
                cmd="train",
                env=env_vars
            )
        else:
            train_model(
                working_dir=dir,
                docker_tag=tag,
                image_name=image_name,
                entrypoint="src/container/executor.sh",
                cmd="train",
                env=env_vars
            )

        logger.info("Local training completed successfully!")
    except ValueError:
        logger.error("This is not a mldock directory: {}".format(dir))
        sys.exit(-1)
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

@click.command()
@click.option('--dir', help='Set the working directory for your mldock container.', required=True)
@click.option('--tag', help='docker tag', type=str, default='latest')
@click.option('--port', help='host url at which model is served', type=str, default='8080')
@click.option('--stage', default='dev', help='environment to stage.', required=True)
@click.pass_obj
def deploy(obj, dir, tag, port, stage):
    """
    Command to deploy ML model(s) locally
    """
    helper_library_path=obj['helper_library_path']
    mldock_manager = MLDockConfigManager(
        filepath=os.path.join(dir, ".mldock.json")
    )
    # get mldock_module_path name
    mldock_config = mldock_manager.get_config()
    module_path = os.path.join(
        dir,
        mldock_config.get("mldock_module_dir", "src"),
    )
    image_name = mldock_config.get("image_name", None)
    platform = mldock_config.get("platform", None)
    container_dir = mldock_config.get("container_dir", None)
    helper_library_path = obj['helper_library_path']
    hyperparameters_env_var = _format_dictionary_as_env_vars(
        {'hyperparameters': mldock_config.get('hyperparameters', {})}
    )
    project_env_vars = _format_dictionary_as_env_vars(mldock_config.get('environment', {}))
    env_vars={
        'stage': stage,
        **hyperparameters_env_var,
        **project_env_vars
    }
    try:
        logger.info("Started local deployment at {}...\n".format(port))
        if platform == "sagemaker":
            deploy_model(
                working_dir=dir,
                docker_tag=tag,
                image_name=image_name,
                port=port,
                entrypoint="container/executor.sh",
                cmd="serve",
                env=env_vars
            )
        elif platform == "sagemakerv2":
            deploy_model(
                working_dir=dir,
                docker_tag=tag,
                image_name=image_name,
                port=port,
                entrypoint="src/container/executor.sh",
                cmd="serve",
                env=env_vars
            )
        else:
            deploy_model(
                working_dir=dir,
                docker_tag=tag,
                image_name=image_name,
                port=port,
                entrypoint="src/container/executor.sh",
                cmd="serve",
                env=env_vars
            )

    except ValueError:
        logger.error("This is not a mldock directory: {}".format(dir))
        sys.exit(-1)
    except subprocess.CalledProcessError as e:
        logger.debug(e.output)
        raise
    except Exception as e:
        logger.error("{}".format(e))
        sys.exit(-1)

local.add_command(build)
local.add_command(predict)
local.add_command(train)
local.add_command(deploy)

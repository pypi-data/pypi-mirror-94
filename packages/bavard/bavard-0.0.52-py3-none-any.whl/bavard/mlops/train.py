"""Script to be called by the pipeline training docker container. Trains a pipeline instance.
"""
import argparse
import logging
import json
import os
import shutil
from uuid import uuid4

import tensorflow as tf
from bavard_ml_common.mlops.pub_sub import PubSub
from bavard_ml_common.mlops.gcs import GCSClient

from bavard.mlops.pipeline import ChatbotPipeline
from bavard.mlops.gcs import download_agent_data
from bavard.dialogue_policy.data.agent import Agent
from bavard import config

logging.getLogger().setLevel(logging.DEBUG)


def get_args():
    """Argument parser.

    Returns:
      Dictionary of arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--gcp-project-id',
        type=str,
        required=True)
    parser.add_argument(
        '--agent-uname',
        type=str,
        required=True)
    parser.add_argument(
        '--job-dir',
        type=str,
        required=True,
        help='local or GCS location for writing checkpoints and exporting models')
    parser.add_argument(
        '--bucket-name',
        type=str,
        required=True)
    parser.add_argument(
        '--export-key',
        type=str,
        required=True)
    parser.add_argument(
        '--publish-id',
        type=int,
        required=False)
    parser.add_argument(
        '--verbosity',
        choices=['DEBUG', 'ERROR', 'FATAL', 'INFO', 'WARN'],
        default='INFO')
    parser.add_argument(
        '--auto',
        choices=['True', 'False'],
        default='True',
        help='whether to automatically determine the training set up for the ML model')
    parser.add_argument(
        '--pipeline-config',
        type=json.loads,
        default=None,
        required=False,
        help='JSON string specifying any additional overriding configuration to use for the NLU pipeline')
    args, _ = parser.parse_known_args()
    return args


def train_and_evaluate(args):
    """Trains and evaluates the Keras model.

    Trains and serializes an `MLModel` instance to the path defined in part
    by the --job-dir argument.

    Args:
      args: dictionary of arguments - see get_args() for details
    """
    # Retreive agent.
    if config.IS_TEST:
        agent_filename = os.path.join(args.bucket_name, args.export_key)  # agent is local
    else:
        agent_filename = download_agent_data(
            bucket_name=args.bucket_name, export_file_key=args.export_key
        )  # agent is in GCS
    agent = Agent.parse_file(agent_filename)

    # Determine pipeline config.
    pipeline_config = {} if args.pipeline_config is None else args.pipeline_config
    if "nlu" not in pipeline_config:
        pipeline_config["nlu"] = {}
        # There is a special CLI arg for specifying the NLU auto parameter.
        pipeline_config["nlu"]["auto"] = args.auto == "True"

    # Create and train the pipeline.
    model = ChatbotPipeline(pipeline_config)
    model.fit(agent)

    # Save to final local or GCS path
    if GCSClient.is_gcs_uri(args.job_dir):
        # First, save to local directory, then upload that directory to GCS.
        temp_dir = str(uuid4())
        os.makedirs(temp_dir)
        model.to_dir(temp_dir)
        GCSClient().upload_dir(temp_dir, args.job_dir)
        # Clean up the local copy.
        shutil.rmtree(temp_dir)
    else:
        model.to_dir(args.job_dir, overwrite=True)

    # Publish job complete message.
    pubsub_msg = {
        'EVENT_TYPE': 'ML_TRAINING_JOB_COMPLETE',
        'SAVED_MODEL_DIR': args.job_dir,
        'AGENT_UNAME': args.agent_uname
    }
    if args.publish_id is not None:
        pubsub_msg['PUBLISH_ID'] = args.publish_id

    print('Publishing message to topic chatbot-service-training-jobs:', str(pubsub_msg))
    if not config.IS_TEST:
        PubSub(args.gcp_project_id).publish('chatbot-service-training-jobs', pubsub_msg)
    print('Published JOB_COMPLETE message')


if __name__ == '__main__':
    args = get_args()

    try:
        tf.compat.v1.logging.set_verbosity(args.verbosity)
        train_and_evaluate(args)
    except Exception as e:
        # Publish job failed message.
        data = {
            'EVENT_TYPE': 'ML_TRAINING_JOB_FAILED',
            'AGENT_UNAME': args.agent_uname
        }
        if args.publish_id is not None:
            data['PUBLISH_ID'] = args.publish_id

        print('Publishing message to topic chatbot-service-training-jobs:', str(data))
        if not config.IS_TEST:
            PubSub(args.gcp_project_id).publish('chatbot-service-training-jobs', data)
        print('Published ML_TRAINING_JOB_FAILED message')
        raise e

# service-monitoring-dag.py file
Created by PD-Core Team - powercore@ge.com, ORG : Power Digital

'''
import json
import logging
import time
import uuid
from datetime import datetime, timedelta
from os.path import realpath, splitext

import requests
from airflow import DAG
from airflow.hooks.http_hook import HttpHook
from airflow.operators import GenieOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator

config_file_path = splitext(realpath(__file__))[0] + "-configuration.json"
with open(config_file_path) as json_file:
    config = json.load(json_file)

# DAG specific parameters and variables
dag_name = "{application_name}-{deployment_name}".format(application_name=config["application_name"].title(),
                                                         deployment_name=config["deployment_name"])

airflow_job_id = "AIRFLOW-" + "{dag_name}-{uuid}".format(dag_name=dag_name, uuid=str(uuid.uuid4()))

start_date = datetime(config["airflow"]["scheduler"]["start_date"]["year"],
                      config["airflow"]["scheduler"]["start_date"]["month"],
                      config["airflow"]["scheduler"]["start_date"]["day"],
                      config["airflow"]["scheduler"]["start_date"]["hour"],
                      config["airflow"]["scheduler"]["start_date"]["minute"],
                      config["airflow"]["scheduler"]["start_date"]["second"]
                      )
genie_conn_id = config["genie"]["genie_conn_id"]
depends_on_past = False if config["airflow"]["scheduler"]["depends_on_past"] in ["False", "false"] else True
dag_default_args = {
    'owner': config["namespace"],
    'airflow_conn_id': genie_conn_id,
    'depends_on_past': depends_on_past,
    'start_date': start_date,
    'end_date': None,
    'email': 'notused@ge.com',
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(seconds=30),
    'queue': config["airflow"]["scheduler"]["queue"],
    'priority_weight': config["airflow"]["scheduler"]["priority_weight"],
    'pool': None if config["airflow"]["scheduler"]["pool"] in ["None", "none"] else config["airflow"]["scheduler"][
        "pool"]
}
schedule_interval = None if config["airflow"]["scheduler"]["schedule_interval"] in ["None", "none"] \
    else config["airflow"]["scheduler"]["schedule_interval"]

build_number = config["build_number"]


def is_application_running(*args, **kwargs):
    config = json.loads(kwargs["config"])
    genie_connection = HttpHook.get_connection('genie')
    url = "{}/api/v3/jobs".format(genie_connection.host)
    application_name_tag = 'application_name:{}'.format(config['application_name'])
    build_number_tag = 'build_number:{}'.format(build_number)

    req_params = {
        "tag": application_name_tag + ',' + build_number_tag,
        "size": "1",
        "sort": "created,desc",
        "status": "RUNNING,INIT"
    }
    response = requests.request("GET", url, params=req_params)
    running_jobs = int(json.loads(response.text)['page']['totalElements'])
    logging.info("Found {} jobs for the application {} and build {}".format(running_jobs, config['application_name'],
                                                                            build_number))
    if running_jobs > 0:
        return True
    else:
        return False


def find_branch(*args, **kwargs):
    is_app_already_running = is_application_running(*args, **kwargs)
    if is_app_already_running:
        return 'monitor_{application}'.format(application=config['application_name'])
    else:
        return 'launch_{application}_and_monitor'.format(application=config['application_name'])


def check_if_app_needs_relaunch(operator, *args, **kwargs):
    """
    Pre-processor hook for Genie operator. Double checks if service is already running on Genie.
    This is needed if the Airflow worker where this task was running shuts down and a new node is re-launched.
    This check will make sure the same service with the same build is not launched to Genie.
    """
    is_app_running = is_application_running(*args, **kwargs)
    needs_relaunch = not is_app_running
    return needs_relaunch


def monitor(*args, **kwargs):
    """This function waits on the current running genie job.
    """
    config = json.loads(kwargs["config"])
    genie_connection = HttpHook.get_connection('genie')
    url = "{}/api/v3/jobs".format(genie_connection.host)
    application_name_tag = 'application_name:{}'.format(config['application_name'])
    build_number_tag = 'build_number:{}'.format(build_number)

    req_params = {
        "tag": application_name_tag,
        "tag": build_number_tag,
        "size": "1",
        "sort": "created,desc",
        "status": "RUNNING,INIT"
    }

    logging.info("monitor : Monitoring application {}.".format(config['application_name']))
    while True:
        response = requests.request("GET", url, params=req_params)
        running_jobs = int(json.loads(response.text)['page']['totalElements'])
        if running_jobs == 0:
            logging.info("monitor : Seems application {} was stopped. Exiting...".format(config['application_name']))
            break
        else:
            time.sleep(30)


dag = DAG(dag_name,
          default_args=dag_default_args,
          start_date=start_date,
          schedule_interval=schedule_interval,
          concurrency=config["dag_concurrency"],
          max_active_runs=config["max_active_runs"])

branching_task = BranchPythonOperator(
    task_id='is_{application}_running'.format(application=config["application_name"]),
    python_callable=find_branch,
    op_kwargs={
        "config": json.dumps(config)
    },
    dag=dag)

closing_task = DummyOperator(
    task_id='closing_task',
    trigger_rule='all_done',
    dag=dag)

monitor_current_running_job_task_option = PythonOperator(
    task_id='monitor_{application}'.format(application=config["application_name"]),
    retries=config["genie"]["genie_retries"],
    retry_delay=timedelta(seconds=config["genie"]["genie_retry_interval_seconds"]),
    provide_context=True,
    python_callable=monitor,
    op_kwargs={
        "config": json.dumps(config)
    },
    dag=dag)
monitor_current_running_job_task_option.set_upstream(branching_task)
monitor_current_running_job_task_option.set_downstream(closing_task)

send_to_genie_task_option = GenieOperator(
    task_id='launch_{application}_and_monitor'.format(application=config["application_name"]),
    cluster_tags=config["genie"]["cluster_tags"],
    command_tags=config["genie"]["command_tags"],
    retries=config["genie"]["genie_retries"],
    retry_delay=timedelta(seconds=config["genie"]["genie_retry_interval_seconds"]),

    command_arguments=" --name={app_name} ".format(app_name=config["application_name"]).join(["--conf {key}={value}".format(key=key, value=value) for key, value in
                                config["genie"]["spark_configs"].iteritems()]) + " " + config["genie"][
                          "command_arguments"],

    description='Launch application on Spark: tenant {tenant}, namespace {namespace}, application {application}'.format(
        tenant=config["tenant"], namespace=config["namespace"],
        application=config["application_name"]),
    job_name=airflow_job_id,
    tags=['application_name:{}'.format(config["application_name"]),
          'build_number:{}'.format(build_number)
          ],
    timeout=config["genie"]["job_timeout_seconds"],
    dependencies=config["genie"]["genie_application_dependencies"],
    xcom_vars=dict(),
    python_pre_processor=check_if_app_needs_relaunch,
    op_kwargs={
        "config": json.dumps(config)
    },
    dag=dag)
send_to_genie_task_option.set_upstream(branching_task)
send_to_genie_task_option.set_downstream(closing_task)

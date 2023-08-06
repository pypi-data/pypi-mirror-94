from azure.identity import ClientSecretCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import RunFilterParameters
import time
import functools as ft
import inflection
# import yaml
# from datetime import datetime, timedelta
# import time
# import os, sys


def authenticate(clientid, secret, tenant):
    """
    Wraps the ClientSecretCredential object. Handle these values with care! Best practice is to securely set them as environment variables in CI/CD pipelines or non-source control managed configs if testing locally.
    """
    credentials = ClientSecretCredential(
        client_id=clientid, 
        client_secret=secret, 
        tenant_id=tenant
    )
    return credentials


def connect_to_df(credentials, subscription_id):
    """
    This connects to the specified data factory instance.
    """
    adf_client = DataFactoryManagementClient(credentials, subscription_id)
    return adf_client

def create_pipeline_run(adf_client, pipeline_args):
    """
    This creates a pipeline run. Pipeline_args are resource_group_name,factory_name, pipeline_name and optional parameters={}
    """
    run_response = adf_client.pipelines.create_run(**pipeline_args)
    return run_response

def monitor_pipeline_run(adf_client, get_run_args):
    "This returns a specific pipeline run for use in other functions. Get_run_args are resource_group_name, factory_name, and run_id. Get the run_id after creating the pipeline_run using create_pipeline_run then pass the get_run_args variable to this function."
    pipeline_run = adf_client.pipeline_runs.get(**get_run_args)
    return pipeline_run

def wait_for_pipeline_to_finish(adf_client, get_run_args):
    """
    This simply waits for a pipeline to finish. Pass the data factory client along with the get_run_args including the specific run id. That will get passed to the internal instance of moinitor_pipeline_run.
    """
    i = 1
    pipeline_run = monitor_pipeline_run(adf_client, get_run_args)
    while pipeline_run.status in ["Queued", "InProgress", "Canceling"]:
        time.sleep(10)
        print("loop #%s" % i)
        print(pipeline_run.status)
        pipeline_run = monitor_pipeline_run(adf_client, get_run_args)
        i+=1
    print(pipeline_run.status)
    return pipeline_run.status

def get_specific_activity(adf_client, get_run_args, activity_name):
    """
    This queries the a specific pipeline run and returns a dictionary representation of the activity under test. Get_run_args will need the run_id of the specific pipeline run. The activity name needs to be unique and a valid string.
    """
    pipelinerun = monitor_pipeline_run(adf_client, get_run_args)
    filters = RunFilterParameters(last_updated_after=pipelinerun.run_start, last_updated_before=pipelinerun.run_end)
    factoryname = get_run_args['factory_name']
    resourcegroup = get_run_args['resource_group_name']
    activityruns = adf_client.activity_runs.query_by_pipeline_run(
    factory_name = factoryname,
    run_id= pipelinerun.run_id,
    filter_parameters = filters,
    resource_group_name = resourcegroup)
    activity_search = [x.as_dict() for x in activityruns.value if x.as_dict()['activity_name'] == activity_name]
    if activity_search == []:
        print("No activity with name {} found.".format(activity_name))
        return
    elif len(activity_search)>1:
        print("More than one activity found with name {}. Name your activities more specifically.".format(activity_name))
        return
    elif len(activity_search) == 1:
        print("Activity {} found".format(activity_name))
        activity = activity_search[0]
        return activity
    else:
        print("Something else went randomly wrong in looking for activity {}.".format(activity_name))
        return

def get_activity_attribute(activity, attribute_search):
    """
    This returns the requested attribute from the activity dictionary. The attribute can be of any arbitrary depth but must be passed as a list. For example: ["output", "writeRows"]. 
    """
    if type(attribute_search) == str:
        attribute = activity[attribute_search]
        return attribute
    elif type(attribute_search) == list:
        attribute = ft.reduce(lambda val, key: val.get(key) if val else None, attribute_search, activity)
        return attribute
    else:
        print("Need to pass str or list for attribute_search")
        return

def process_attribute_search_string(attribute_search_base):
    """
    This processes string input into ouput that can then be input into the get_activity_attribute function. The function processes strings like '[Output, rowsWritten]' to a list like ['Output', 'rowsWritten']
    """
    if "[" in attribute_search_base:
        attribute_search = list(map(str, attribute_search_base.strip('[]').split(',')))
        attribute_search = [x.replace(" ", "") for x in attribute_search]
    elif "[" not in attribute_search_base:
        attribute_search = attribute_search_base
    else:
        print("Invalid construction for attribute search passed, setting attribute search to None")
        attribute_search = None   
    return attribute_search

def get_linked_service(adf_client, resource_args):
    """
    This returns a LinkedServiceResource object from the currently defined azure datafactory connection.
    """
    linked_service = adf_client.linked_services.get(**resource_args)
    return linked_service


def get_dataset(adf_client, resource_args):
    """
    This returns a DatasetResource object from the currently defined azure datafactory connection.
    """
    dataset = adf_client.datasets.get(**resource_args)
    return dataset

def get_pipeline(adf_client, resource_args):
    """
    This returns a PipelineResource object from the currently defined azure datafactory connection.
    """
    pipeline = adf_client.pipelines.get(**resource_args)
    return pipeline

def check_resource_name(name, resource):
    return name == resource.name


def get_parameters(resource):
    if 'parameters' not in dir(resource):
        if 'properties' in dir(resource):
            parameters = resource.properties.parameters
        else: 
            parameters = "Phoink"
    elif 'parameters' in dir(resource):
        parameters = resource.parameters
    else:
        parameters = 'Phoink'
    return parameters

def process_out_inner_objects(raw_object):
    processed_object = {key:(raw_object[key].__dict__ if '__dict__' in dir(raw_object[key]) else raw_object[key]) for key in raw_object.keys()}
    return processed_object

def underscore_camelcase_inner_keys(from_dict):
    to_dict = {
          key:{
               inflection.underscore(inner_key): from_dict[key][inner_key] for inner_key in from_dict[key]
          } for key in from_dict.keys()
     }
    return to_dict

def harmonize_dictionary_keys(keys_1, keys_2):
    return set(keys_1).intersection(keys_2)

def return_inner_keys(from_dict):
    inner_keys = [inner_key for key in from_dict.keys() for inner_key in list(from_dict[key].keys()) ]
    return inner_keys

def rebuild_inner_dict_with_common_keys(compare_dict, common_keys):
    rebuilt_dict = {
          key:{
               inner_common_key: compare_dict[key][inner_common_key] for inner_common_key in common_keys
          } for key in compare_dict.keys()
     }
    return rebuilt_dict

 # Project Name

 adftestpy

 # Description

 This python library is a lightweight setup of helper functions designed to help developers write unit tests against Microsoft's Azure Data Factory PAAS. 

 # Installation

 For finished package:  

    pip install adftestpy

For GitHub Repo clone to your editor of choice. 

# Function Documentation

Requirements for each function are maintained in the corresponding function itself. 

# Philosophy

Azure Data Factory, being PAAS, does not provide the same level of "testability" that software developed in a programming langauge does. As of this writing, configurations are specified in the UI or underlying JSON and published to Azure customer's Data Factory instances. This means that the unit of test, rather than being a method or function, can be instead thought of as an activity running in a single pipeline. Pipeline runs can be created programmatically through the Azure Python SDK and retrieved from that same SDK. Specific activity runs in that specific pipeline run can be further retrieved from there. Those specific activity runs can be converted into python dictionaries. The resulting python dictionary result can be asserted against an expected condition to produce a succeeding or failing unit test. 

# Data Factory Setup Requirements

To perform unit testing utilizing best practices such as dependency injection, the Data Factory instance must be setup to support those practices. 

Dependency injection in this case means _providing settings dynamically to a given pipeline for a given pipeline run_. 

This requires that many things be parameterized in the Data Factory service such as but not limited to:

- Linked Services
- Datasets
- Pipelines
- Specific Activities

## Overall components and flow

A dependency injection enabled pipeline will consist of sevearal components. 

1. One or more parameterized linked services
2. One or more parameterized datasets that reference those parameterized linked services.
3. A pipeline with pipeline variables, ideally starting with `__` to indicate they are for the purposes of dependency injection, that map to the requirements of the parameterized datasets. 

Flow:

Pipeline variables -> Dataset variables -> Linked Service variables

### Linked Services

See Microsoft's documentation about how to parameterize a linked service 
[here](https://docs.microsoft.com/en-us/azure/data-factory/parameterize-linked-services).

Not noted in that piece of documentation as of this writing is a soft limit on how many type properties can be parameterized. As of this writing, four type properties can be parameterized before the linked service fails to resolve.

Be advised that JSON editing may be required depending on what linked service is required. 

Connection strings and service principal components (id, Azure Key Vault Secret Name pointing to id, Azure Key Vault Secret Name pointing to secret, etc) are prime candidates for parameterization. 

### Datasets

Datasets support parameterization more commonly than linked services and are parametrized (dynamic content filled in for requirements) in a similar way. 

### Pipelines

Pipelines support parameterization via defining pipeline variables. As stated before ideally these variables begin with `_` to denote their usage for dependency injection. 

### Specific Activities

Different activities support different levels of parameterization. The Copy Activity for example, is very friendly because a dataset can be selected and the corresponding pipeline variables can be reference. An Azure Data Explorer command on the other hand is significantly less friendly, as only the command input accepts dynamic content as of this writing. 


# Usage Example

These functions simply retrieve the specific results of a specific configuration in Azure Data Factory. Therefore they can be used in any python test framework desired. However, the following example will be written for _pytest_. This example will also assume that these tests will be executed in a CI/CD tool like Azure Dev Ops or GitHub Actions. Local development has slightly different requirements.

## General Test Format

In general tests can be constructed simiarly to testing other software components. The developer defines the assertion criteria then tests the results of the appropriate helper function against it. The only difference here being the retrieval of the specific pipeline activity from a specific pipeline run to form the element that is tested against the assertion criteria. 

Here is an example of a written unit test:

    def test_pipeline_activity_general(load_configs, azure_data_factory_service_connection, complete_pipeline_run, pipeline_name_set):
        test_configs = load_configs
        pipeline_name = pipeline_name_set
        adf_client = azure_data_factory_service_connection
        activity_name = "My Activity"
        test_type = 'general'
        to_test_attribute = test_configs['Pipeline Configs'][pipeline_name]['activities'][activity_name][test_type]['totest']
        attribute_search = helpers.process_attribute_search_string(to_test_attribute)
        get_run_args = complete_pipeline_run
        activity = helpers.get_specific_activity(adf_client, get_run_args, activity_name)
        to_assert = test_configs['Pipeline Configs'][pipeline_name]['activities'][activity_name][test_type]['toassert']
        to_test = helpers.get_activity_attribute(activity, attribute_search)  
        assert to_assert == to_test

Each arguments passed into the test function is a test fixture either run on the session scope from a _conftest.py_ file existing in the same directory as the tests or a test fixture run on the module scope in the test file itself. For more information see the pytest [documentation](https://docs.pytest.org/en/stable/fixture.html). 

_test_configs_ is a dictionary read from a YAML file whose specification will be described below. 

_pipeline_name_ is a string resulting from a test fixture in the same file as the test run at the module scope:

    @pytest.fixture(scope='module')
    def pipeline_name_set():
        pipeline_name = "My Pipeline"
        return pipeline_name

_adf_client_ is the connection to your Azure Data Factory instance resulting from a test fixture run from the _conftest.py_ file with the session scope. 

    @pytest.fixture(scope='session')
    def azure_data_factory_connection(azure_connection):
        subscription = os.environ.get("SPN_SUBSCRIPTION")
        adf_client = helpers.connect_to_df(azure_connection, subscription)
        return adf_client

The Azure Subscription is set securely as an environment variable before test execution. See CI/CD section for more discussion of the examples provided in this repo.

The `helpers.connect_to_df function` requires an azure connection to be passed along with the subscription. That is created from another test fixture existing in the _conftest.py_ file with the session scope. 

    @pytest.fixture(scope='session')
    def azure_connection(load_environment_variables):
        service_principal_args = {
            "clientid": os.environ.get("SPN_KEY"),
            "secret": os.environ.get("SPN_SECRET"),
            "tenant" : os.environ.get("SPN_TENANT")
            }
        credentials = helpers.authenticate(**service_principal_args)
        return credentials

The Service Principal Key (Client Id), Secret, and Tenant are all securely set as environment variables in the CI/CD process. The `load_environment_variables` fixture is a fixture not returning any values in the CI/CD process. It is used only for local development. The credentials object is created then used downstream. 

_activity_name_ is the name of the specific activity fetched and tested. This is definited on a test by test basis. 

_test_type_ stores what type of test is being performed and is defined on a test by test basis. As of this writing two different types of tests are supported: _general_ and _copy_. General refers to a general test of success/failure for any activity in an Azure Data Factory pipeline. Copy refers specifically to tests of a given Copy Activity asserting that the rowsRead property of the input == the rowsCopied property of the output. The specifications of these tests are further defined in the _test_configs.yml_ file specification. 

_to_test_attribute_ is the attribute whose value will be asserted against the _to_assert value to determine pass or fail. This is loaded from the _test_configs.yml_ file. 

_attribute_search_ is the _str_ or _list_ value that will be searched for in the actual activity JSON response. _List_ values are processed from a _str_ specified in the _test_configs.yml_ file. This is processed by the `helpers.process_attribute_search_string` function.

_get_run_args_ is a dictionary of required arguments for the `helpers.get_specific_activity` function. This is returned from a test fixture called `complete_pipeline_run` that is run in the same test file as this test with the module scope. 

    @pytest.fixture(scope='module')
    def complete_pipeline_run(load_configs, pipeline_name_set, azure_data_factory_service_connection):
        test_configs = load_configs
        adf_client = azure_data_factory_service_connection
        pipeline_name = pipeline_name_set
        pipeline_args = test_configs['Pipeline Configs'][pipeline_name]['pipeline_args']
        pipeline_args['pipeline_name'] = pipeline_name
        pipeline_args['parameters'] = test_configs['Pipeline Configs'][pipeline_name]['parameters']
        get_run_args = test_configs['Pipeline Configs'][pipeline_name]['get_run_args']
        pipeline_run = helpers.create_pipeline_run(adf_client, pipeline_args)
        get_run_args['run_id'] = pipeline_run.run_id
        helpers.wait_for_pipeline_to_finish(adf_client, get_run_args)
        return get_run_args

_activity_ is the JSON response of the specified activity in the completed pipeline. 

_to_assert_ and _to_test_ are the actual conditions checked in the assert statement. _to_assert_ is defined in the `test_configs.yml` file. _to_test_ is set by the `helpers.get_activity_attribute` method requiring the activity and the attribute search value defined earlier. 

Finally, the assert statement implements that actual pass/fail mechanics of the test. 

## Test Configurations

### Unit Test In Editor Configs

See your editor of choice's instructions for how to configure tests to show up in your editor. For VS Code, pay special attention to your python virtual environment being started up properly. 

### test_configs.yml

This is a yaml file where repeatable configurations for your tests are stored. These are loaded into the test function and ran when running your tests locally or on a CI/CD agent. YAML is compiled into a python dictionary at run-time. See [here](https://learnxinyminutes.com/docs/yaml/) for the basics of YAML authoring. An example of this exists in the `test` directory of this repository as it is necessary to test the helper functions themselves.

The file consits of two main parts: Common and Pipeline Configs. 

#### Common

This section contains argument groups that will be necessary for each and every pipeline you test. Three groupings are shipped: `pipeline_args`, `get_run_args`, and a broader section called `unit test requirements`. Generous use of anchors reduce re-typing of configs across the document. `pipeline_args` contains the repeatable arguments necessary to run a pipeline, such as `factory_name` and `resource_group_name`. `get_run_args` repeats those same defined arguments for later addition of run specific args (see above). The `unit rest requirements` section contains the requirements for each type of unit test: general and copy. 

#### Pipeline Configs

This section is organized as follows:
```
Pipeline Configs:
    PIPELINE NAME:
        pipeline_args: *pipeline_args
        get_run_args: *get_run_args
        parameters:
            Param1: My Param
            Param2: My Param2
        activities:
            ACTIVITY NAME:
                TEST TYPE: *TEST TYPE CONFIGS
```


### conftest.py

This is a fixtures file as defined by the pytest documentation [here](https://docs.pytest.org/en/stable/fixture.html). Write your session level fixtures here for use in the entire testing session. Examples of these are connecting to Azure, connecting to your ADF instance, etc.

#### load_environment_variables fixture

This is a special fixture used to load specific environment variables from a yaml file stored **outside** the development directory and **outside** of source control. The path to that config file is stored at the system level in AZURE_DATA_FACTORY_TESTING_CONFIG.

````
def load_environment_variables():
    if "COMPUTERNAME" in os.environ:
        local_machine = os.environ.get("COMPUTERNAME") == os.environ.get("AZURE_DATA_FACTORY_TEST_COMPUTER")
    else:
        local_machine = False
    if local_machine:
        filename = os.environ.get("AZURE_DATA_FACTORY_TESTING_CONFIG")
        file = open(filename, encoding='utf-8')
        yml = yaml.full_load(file)
        os.environ["SPN_KEY"] = yml['Service Principal']['Key']
        os.environ["SPN_SECRET"] = yml['Service Principal']['Secret']
        os.environ["SPN_TENANT"] = yml['Service Principal']['Tenant']
        os.environ['SPN_SUBSCRIPTION'] = yml['Service Principal']['Subscription']
        return yml
    else:
        return
````

The fixture checks the COMPUTERNAME environment variable (found in Windows Machines) against a defined AZURE_DATA_FACTORY_TEST_COMPUTER variable. This variable must be defined at the system level for python to recognize it. If true, then it loads as environment variables the SPN_KEY, SPN_SECRET, SPN_TENANT, and SPN_SUBSCRIPTION. These will be used in the rest of the tests. 

The YAML file is structured as follows:

```
Service Principal:
    Key: My Key
    Secret: My Secret
    Tenant: My Tenant
    Subscription: My Subscription
```

# Isolating System Under Test

In order to evaluate the configurations by themselves without relying on the source systems, it is recommended that the unit tests be run against abridged copies of the data sources and sinks that the development team controls. These will perform the function of stubs in this context. 

# Test Nomenclature

Two recommendations for naming tests:

1. Conform to prefix, suffix, rules for your test framework. 
2. Include the pipeline name in the name of the test file. 

# Test Organization

It is recommended that all tests for a single pipeline are included in one file and one file only. 

# Pipeline Organization

Simplicity lies at the heart of good unit testing. To this end, it is recommended that developers isolate the core data movement activities into `meta pipelines` that are called with specific pipeline paramaters for the specific act of data movement needing execution and testing. 

# CI/CD Pipeline Example Discussions

Azure Resource secrets should not be exposed in source controlled code. Example files are included for two different CI/CD systems: [Azure DevOps Pipelines](https://docs.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops) and [GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions/learn-github-actions/introduction-to-github-actions).

## Azure DevOps

See azure_devops_pipeline_example.yml for actual configuration. This example is intended to run on the `ubuntu-latest` pool. Secrets intended for exporting as environment variables should be stored in Azure Key Vault and linked to an appropriate Azure DevOps Variable Group. Then that variable group can be referenced in the .yml configuration. From there the example contains both the test directory name and test xml output file names as variables for later use. The pipeline is set in Azure DevOps to continue on error in order that test results will be fully published. The example then operates with four steps, setting the python version to 3.x, installing the required packages, running the tests, then publishing junit style test results to Azure DevOps. The results of that tests will be visible in the `Test Plans` section of Azure DevOps. 

## GitHub Actions

The GitHub Actions example is actually the workflow used in this very repo. See .github/test-library.yml. This workflow runs the unit tests of the actual functions. After setting up python and checking out the repo, the example installs the required packages and runs the tests. At this time no test reporting is done with GitHub Actions for this repo. 


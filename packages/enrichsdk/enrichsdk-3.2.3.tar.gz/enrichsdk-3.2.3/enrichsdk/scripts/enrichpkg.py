#!/usr/bin/env python3

# Core
import os
import sys
import pip
import base64
import subprocess
import json
import imp
import yaml
import traceback
import pkg_resources
import logging, traceback
import pyfiglet

# thirdparty
import click
from pythonjsonlogger import jsonlogger

# self
import enrichsdk
from enrichsdk import package, datasets, api as sdkapi, lib, featurestore as fslib

@click.group()
def process():
    """
    Bootstrap/test/install Enrich modules and access server

    \b
    Getting started:
       version:  Version of this sdk
       start:    First time instructions
       env:      Setup the environment context

    \b
    Development:
       bootstrap:  Bootstrap modules including transforms
       test:      Test transforms, manage datasets

    \b
    Server:
       api:       Access the server API

    \b
    Helpers:
       show-log:  Pretty print log output
    """
    pass

@click.command('version', hidden=True)
def _version():
    """
    Show version
    """
    print(enrichsdk.__version__)

@click.command('start', hidden=True)
@click.option('--commands/--no-commands',
              default=False,
              help="Show commands")
def _start(commands):
    """
    Instructions to get started
    """

    result = pyfiglet.figlet_format("Enrich SDK", font = "slant"  )
    print(result)

    home = os.environ['HOME']
    if 'VIRTUAL_ENV' not in os.environ:
        print("SDK not installed in virtual environment")
        return

    if "ENRICH_ROOT" in os.environ:
        enrich_root = os.environ['ENRICH_ROOT']
    else:
        enrich_root = "$ENRICH_ROOT"
    venv_root = os.environ['VIRTUAL_ENV']
    venv_name = os.path.basename(venv_root)

    steps = [
        {
            "description": "Understand Enrich and SDK",
        },
        {
            "description": "set ENRICH_ROOT and populate",
            "cmd": [
                "export ENRICH_ROOT={}/work/enrich".format(home),
                "mkdir -p $ENRICH_ROOT",
                "enrichpkg env populate"
            ]
        },
        {
            "description": "Check and update siteconf and versionmap",
            "cmd": [
                "enrichpkg env check",
                "cat $ENRICH_ROOT/etc/siteconf.json",
            ]
        },
        {
            "description": "[OPTIONAL] For complex deployments, create an environment/context file",
            "cmd": "enrichpkg env sample-context > context.yaml",
        },

        {
            "description": "[OPTIONAl] Create a simple settings file",
            "cmd": [
                '# file to be sourced before you start working. use the appropriate',
                '# environment activation mechanism',
                'echo "#source {}/bin/activate" > $ENRICH_ROOT/env.sh'.format(venv_root),
                'echo "workon {}" >> $ENRICH_ROOT/env.sh'.format(venv_name),
                'echo "export ENRICH_ROOT={}" >> $ENRICH_ROOT/env.sh'.format(enrich_root)
            ]
        },
        {
            "description": "Change dir to $ENRICH_CUSTOMERS",
            "cmd": "cd $ENRICH_ROOT/customers",
        },
        {
            "cmd": [
                "#To handle python paths etc. avoid spaces and hyphen in the names",
                "git checkout git@github.com:alphainc/enrich-acme.git acme"
            ],
            "description": "GIT checkout a code repository"
        },
        {
            "cmd": "cd $ENRICH_ROOT/customers/acme",
            "description": "Change to checked out repository"
        },
        {
            "cmd": [
                "enrichpkg bootstrap -c repo -p ."
            ],
            "description": "Bootstrap the repo if not already done"
        },
        {
            "cmd": [
                "# Typically usecases have first letter in capital",
                "enrichpkg bootstrap -c usecase -p Marketing"
            ],
            "description": "Create usecase, say Marketing"
        },
        {
            "cmd": [
                "cd Marketing"
            ],
            "description": "Change to usecase"
        },
        {
            "description": "Bootstrap a transform",
            "cmd": [
                "# Will create a python script",
                "enrichpkg bootstrap -c transform-simple -p transforms/helloworld.py",
                "# Will create a python module",
                "enrichpkg bootstrap -c transform-simple -p transforms/helloworld",
                "# Will create a python package",
                "enrichpkg bootstrap -c transform-package -p transforms/helloworld",
                "# Will create a hello world script",
                "enrichpkg bootstrap -c transform-helloworld -p transforms/helloworld.py",
            ]
        },
        {
            "cmd": [
                "# Add any requirements and install them",
                "vi ../requirements.txt",
                "pip install -r ../requirements.txt",
            ],
            "description": "Install repo-specific requirements"
        },
        {
            "cmd": [
                "enrichpkg test transform transforms/helloworld.py",
                "# To capture all debug logs",
                "enrichpkg test transform --capture transforms/helloworld.py",
            ],
            "description": "Test the transform"
        },
        {
            "cmd": [
                "enrichpkg bootstrap -c pipeline-conf -p pipelines/conf/helloworld.py"
            ],
            "description": "Bootstrap a pipeline"
        },
        {
            "cmd": [
                "enrichpkg test conf --capture pipelines/conf/helloworld.py"
            ],
            "description": "Check pipeline"
        },
        {
            "cmd": [
                "# prefect is the default workflow engine",
                "enrichpkg bootstrap -c prefectjob -p workflows/prefect/daily.py"
            ],
            "description": "Bootstrap a Prefect workflow"
        },
        {

            "cmd": [
                "workflows/prefect/daily.py"
            ],
            "description": "Check workflow"
        },
    ]

    if not commands:
        print("Note: Use --commands to see how to implement these steps\n")

    for i, s in enumerate(steps):
        print("[{:2}] {}".format(i+1, s['description']))
        if not commands:
            continue

        print("")
        if 'cmd' in s:
            if isinstance(s['cmd'], str):
                print("    $ {}".format(s['cmd']))
            else:
                for c in s['cmd']:
                    print("    $ {}".format(c))
        print("")


@click.command('bootstrap', hidden=True)
@click.option("--component", '-c',
              required=True,
              help="What should be bootstrapped",
              type=click.Choice(['repo',
                                 'usecase',
                                 'transform-package',
                                 'transform-simple',
                                 'transform-helloworld',
                                 'asset',
                                 'task-lib',
                                 'task-conf',
                                 'pipeline-conf',
                                 'sparkjob',
                                 #'airflow',
                                 'prefectjob',
                                 'rscript',
                                 'pyscript']))
@click.option("--path", '-p',
              required=True,
              help="Directory where the files should be stored")
@click.option("--template", '-t',
              required=False,
              default=None,
              help="Template to override the defaults")
@click.option('--context',
              default=None,
              help="Environment file")
def bootstrap_(component, path, template, context):
    """
    Bootstrap a fresh module
    """

    """
    Modules currently supported include transform, model, and skin.

    For now only the transforms and models are testable locally
    without the need for a test server.

    In future we expect to more comprehensively support the
    development of all modules.

    A custom template can be provided as well.
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        raise
    context.set_env()

    if not package.checkenv(validate_only=True):
        print("Environment is incomplete")
        print("Try: enrichpkg env check")
        return

    package.bootstrap(component, path, template)

@click.command('show-log', hidden=True)
@click.argument('logfile')
def _show_log(logfile):
    """
    Pretty-print run log
    """

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    package.print_log(logfile)

@click.group('env', hidden=True)
@click.pass_context
def envsetup(ctx):
    """
    Setup the environment. Environment includes:\n
      \b
      (a) Workspace for enrich to work
      (b) Minimal configuration

    This can be specified using environment variables
    and/or 'context' file.

    The absolute minimal required environment variable
    is ENRICH_ROOT (path to enrich workspace e.g.,
    ~/enrich)
    """

    ctx.ensure_object(dict)

@envsetup.command('sample-context')
@click.option("--root", '-r',
              default=None,
              help="Root of enrich")
def _context_generate(root):
    """
    Generate sample context file
    """

    if root is not None:
        os.environ['ENRICH_ROOT'] = os.path.abspath(root)
    elif 'ENRICH_ROOT' not in os.environ:
        os.environ['ENRICH_ROOT'] = os.path.expandvars("$HOME/enrich")

    context = lib.Context()
    context = context.asdict()

    if 'siteconf' not in context:
        context['siteconf'] = os.path.join(context['ENRICH_ETC'],
                                           'siteconf.json')

    print("Please store this in context.yaml")
    print("Minimum required valid paths include: siteconf, versionmap, enrich_data")
    print("Example: enrichpkg api --context context.yaml ...")
    print("----")
    print(yaml.dump(context, indent=4))

@envsetup.command('sample-versionmap')
def _versionmap():
    """
    Generate sample versionmap
    """

    print("Please store this in versionmap.json. Default is $ENRICH_ROOT/etc/versionmap.json")
    print("Update context.yaml with this versionmap path")
    print("----")
    print(package.get_sample_versionmap())

@envsetup.command('sample-siteconf')
def _siteconf():
    """
    Generate sample siteconf
    """

    print("Please store this in siteconf.json. Default is $ENRICH_ROOT/etc/siteconf.json")
    print("Update context.yaml with this siteconf path")
    print("----")
    print(package.get_sample_siteconf())

@envsetup.command('populate')
@click.option("--context",
              default=None,
              help="Context file")
def _populate(context):
    """
    Populate the directories
    """
    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        print("Error! " + str(e))
        return

    context.set_env()

    package.populate(context=context.asdict())

@envsetup.command('check')
@click.option("--context",
              default=None,
              help="Context file")
def _checkenv(context):
    """
    Check environment
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        print("Error! " + str(e))
        return

    context.set_env()

    package.checkenv(context=context)


##########################################################
# Test command
##########################################################
@click.group('test', hidden=True)
@click.option('--context',
              default=None,
              help="Environment file")
@click.pass_context
def test(ctx, context):
    """
    Test transforms/pipelines etc.
    """

    # use the context file to set the environment
    try:
        context = lib.Context(context)
    except Exception as e:
        raise

    context.set_env()
    ctx.ensure_object(dict)
    ctx.obj['context'] = context.asdict()


@test.command('transform')
@click.argument("pkgdir")
@click.option('--capture/--no-capture',
              default=False,
              help="Capture output")
@click.pass_context
def test_pkg(ctx, pkgdir, capture):
    """
    Unit testing of a package module (transform)
    """
    context = ctx.obj['context']

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    package.test_transform(pkgdir, capture, context)

@test.command('task-lib')
@click.argument("taskdir")
@click.option('--capture/--no-capture',
              default=False,
              help="Capture output")
@click.pass_context
def test_task(ctx, taskdir, capture):
    """
    Unit testing of a task library
    """

    context = ctx.obj['context']

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    package.test_task(taskdir, capture, context)

@test.command('conf')
@click.argument("spec")
@click.option('--capture/--no-capture',
              default=False,
              help="Capture output")
@click.pass_context
def test_conf(ctx, spec, capture):
    """
    Minimal testing of pipeline/task configuration
    """

    context = ctx.obj['context']

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    package.test_conf(spec, capture, context)

@click.group("data")
@click.argument("spec")
@click.option('--capture/--no-capture',
              default=False,
              help="Capture output")
@click.pass_context
def testdata(ctx, spec, capture):
    """
    Manage test data


    spec could be transform or a spec file
    """
    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    ctx.ensure_object(dict)
    ctx.obj['spec'] = spec
    ctx.obj['capture'] = capture

@testdata.command('list')
@click.pass_context
def _testdata_list(ctx):
    """
    List available test datasets
    """

    package.testdata_action("list",
                            ctx.obj['spec'],
                            ctx.obj['capture'],
                            ctx.obj['context'])

@testdata.command('show')
@click.argument('dataset')
@click.pass_context
def _testdata_show(ctx, dataset):
    """
    Show the details of a given dataset
    """

    package.testdata_action("show",
                            ctx.obj['spec'],
                            ctx.obj['capture'],
                            ctx.obj['context'],
                            name=dataset)

@testdata.command('run',
                  context_settings=dict(
                      ignore_unknown_options=True,
                      allow_extra_args=True,
                  ))
@click.argument('dataset')
@click.argument('command')
@click.pass_context
def _testdata_action(ctx, dataset, command):
    """
    Generate action commands for a dataset over a specified range

    Pass additional parameters as key-value pairs as
    shown in show.
    """

    args = dict()
    for item in ctx.args:
        args.update([item.split('=')])

    package.testdata_action("action",
                            ctx.obj['spec'],
                            ctx.obj['capture'],
                            ctx.obj['context'],
                            name=dataset,
                            command=command,
                            **args)


test.add_command(testdata)

#########################################
# API
#########################################
@click.group(hidden=True)
@click.option("--config",
              default=None,
              help="API Config File")
@click.pass_context
def api(ctx, config):
    """
    Access Enrich Server
    """

    if not package.checkenv(validate_only=True):
        print("Try: enrichpkg checkenv")
        raise Exception("Environment incomplete")

    alt = os.path.expandvars("$ENRICH_ETC/api.json")
    if config is None:
        config = alt

    # Write a default
    default = {
        "schema": "v1:api:enrich",
        "backends": [
        ]
    }
    if not os.path.exists(config):
        with open(config, 'w') as fd:
            fd.write(json.dumps(default, indent=4))

    ctx.ensure_object(dict)
    ctx.obj['config'] = config

@click.group()
@click.pass_context
def config(ctx):
    """
    Configure access to Enrich Server
    """
    pass

@config.command("init")
@click.pass_context
def _config_init(ctx):
    """
    Initialize the config file
    """
    default = {
        "schema": "v1:api:enrich",
        "backends": [],
        "services": [],
    }
    filename = ctx.obj['config']
    with open(filename, 'w') as fd:
        fd.write(json.dumps(default, indent=4))

    print("Initialized config")

@config.command("list")
@click.pass_context
def _config_list(ctx):
    """
    List available backends/services
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    print("Backends")
    print("-----")
    backends = config['backends']
    for b in backends:
        key = base64.b64decode(b['key'].encode('utf-8')).decode('utf-8')
        try:
            print("{} [{} @ {}]".format(b['name'], key,b['server']))
        except:
            pass

    print("\n")
    print("Services")
    print("-----")
    services = config.get('services',[])
    for s in services:
        try:
            print("{} [{}]".format(s['name'], s['path']))
        except:
            pass

@config.command("backend-add")
@click.argument("name")
@click.argument("server")
@click.argument("key")
@click.pass_context
def _backend_add(ctx, name, server, key):
    """
    Add backend
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    # Encode the key before storing
    key = base64.b64encode(key.encode('utf-8')).decode('utf-8')

    backends = config['backends']
    missing = True
    for b in backends:
        if ('server' in b) and (b['server'] == server):
            b['name'] = name
            b['server'] = server
            b['key'] = key
            missing = False
            break

    if missing:
        backends.append({
            'name': name,
            'server': server,
            'key': key
        })

    with open(filename, 'w') as fd:
        fd.write(json.dumps(config, indent=4))

    print("Added {}".format(name))

@config.command("backend-remove")
@click.argument("name")
@click.pass_context
def _backend_remove(ctx, name):
    """
    Add backend
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    backends = config['backends']
    missing = True
    updated = [b for b in backends if ((b.get('server',None) != name) and
                                       (b.get('name',None) != name))]

    if len(backends) == len(updated):
        raise Exception("Backend not found: {}".format(name))

    config['backends'] = updated

    with open(filename, 'w') as fd:
        fd.write(json.dumps(config, indent=4))

    print("Removed {}".format(name))

@config.command("service-add")
@click.argument("name")
@click.argument("path")
@click.pass_context
def _service_add(ctx, name, path):
    """
    Add URL
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    if 'services' not in config:
        config['services'] = []

    services = config['services']
    missing = True
    for s in services:
        if ('name' in s) and (s['name'] == name):
            s['name'] = name
            s['path'] = path
            missing = False
            break

    if missing:
        services.append({
            'name': name,
            'path': path
        })

    with open(filename, 'w') as fd:
        fd.write(json.dumps(config, indent=4))

    print("Added {}".format(name))

@config.command("service-remove")
@click.argument("name")
@click.pass_context
def _service_remove(ctx, name):
    """
    Remove service
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    services = config['services']
    missing = True
    updated = [s for s in services if s.get('name',None) != name]

    if len(services) == len(updated):
        raise Exception("Service not found: {}".format(name))

    config['services'] = updated

    with open(filename, 'w') as fd:
        fd.write(json.dumps(config, indent=4))

    print("Removed {}".format(name))


@click.group()
@click.argument("backend")
@click.pass_context
def show(ctx, backend):
    """
    Access a backend
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    backends = config['backends']

    relevant = None
    for b in backends:
        if ((b.get('server',None) == backend) or
            (b.get('name',None) == backend)):
            relevant = b
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))

    # Decode the key before accessing
    key = base64.b64decode(relevant['key'].encode('utf-8')).decode('utf-8')
    relevant['key'] = key

    backend = sdkapi.Backend(relevant)
    ctx.obj['backend'] = backend


@show.command("status")
@click.option("--offset", default=0)
@click.option("--page", default=20)
@click.pass_context
def _status(ctx,offset,page):
    """
    Execution status
    """

    backend = ctx.obj['backend']
    result = backend.status(offset,page)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return


    columns = ['usecase', 'nature', 'name', 'status', 'runid', 'start_time', 'duration']
    sdkapi.draw(backend, 'status',
                result, columns)

@show.command("usecases")
@click.pass_context
def _usecases(ctx):
    """
    Show available usecases
    """

    backend = ctx.obj['backend']
    result = backend.usecases()

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return


    columns = ['customer', 'name','description']
    sdkapi.draw(backend, 'usecases',
                result, columns)

@show.command("health")
@click.pass_context
def _health(ctx):
    """
    Show system health
    """

    backend = ctx.obj['backend']
    result = backend.health()

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return


    sdkapi.draw_health(backend, 'health', result)

@show.command("pipelines")
@click.argument('usecase')
@click.pass_context
def _pipelines(ctx, usecase):
    """
    Show available pipelines
    """

    backend = ctx.obj['backend']
    result = backend.pipelines(usecase)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return

    data = result['data']
    for d in data:
        d['description'] = d['description'][:20]
        runs = sorted(d['runs'],reverse=True)
        if len(runs) > 0:
            d['lastrun'] = runs[0]
            d['runs'] = len(runs)
        else:
            d['lastrun'] = ""
            d['runs'] = 0

    columns = ['usecase', 'name','description', 'path', 'runs', 'lastrun']
    sdkapi.draw(backend, 'pipelines',  result, columns,
                {
                    'Usecase': usecase,
                })

@show.command("run-list")
@click.argument('usecase')
@click.argument('pipeline')
@click.pass_context
def _runs(ctx, usecase, pipeline):
    """
    Show available runs for pipeline
    """

    backend = ctx.obj['backend']
    result = backend.run_list(usecase, pipeline)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return

    result['data'] = sorted(result['data'],
                            key=lambda r: r['start_time'],
                            reverse=True)

    columns = ['runid', 'status','start_time', 'end_time']
    sdkapi.draw(backend, 'run-list',  result, columns,
                {
                    'Usecase': usecase,
                    'Pipeline': pipeline
                })

@show.command("run-detail")
@click.argument('usecase')
@click.argument('pipeline')
@click.argument('runid')
@click.pass_context
def _run_detail(ctx, usecase, pipeline, runid):
    """
    Show detail of a given run
    """

    backend = ctx.obj['backend']
    result = backend.run_detail(usecase, pipeline, runid)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return


    sdkapi.draw_run_detail(backend, 'run-detail', result,
                           {
                               'Usecase': usecase,
                               'Pipeline': pipeline,
                               'RunID': runid
                           })

@show.command("tasks")
@click.argument('usecase')
@click.pass_context
def _tasks(ctx, usecase):
    """
    Show available tasks
    """

    backend = ctx.obj['backend']
    result = backend.tasks(usecase)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return

    data = result['data']
    for d in data:
        d['description'] = d['description'][:20]
        runs = sorted(d['runs'],reverse=True)
        if len(runs) > 0:
            d['lastrun'] = runs[0]
            d['runs'] = len(runs)
        else:
            d['lastrun'] = ""
            d['runs'] = 0

    columns = ['usecase', 'name','description', 'path', 'runs', 'lastrun']
    sdkapi.draw(backend, 'tasks',  result, columns,
                {
                    'Usecase': usecase,
                })

@show.command("task-run-list")
@click.argument('usecase')
@click.argument('task')
@click.pass_context
def _task_runs(ctx, usecase, task):
    """
    Show available runs for task
    """

    backend = ctx.obj['backend']
    result = backend.task_run_list(usecase, task)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return

    result['data'] = sorted(result['data'],
                            key=lambda r: r['start_time'],
                            reverse=True)

    columns = ['runid', 'status','start_time', 'end_time']
    sdkapi.draw(backend, 'task-run-list',  result, columns,
                {
                    'Usecase': usecase,
                    'Task': task
                })

@show.command("task-run-detail")
@click.argument('usecase')
@click.argument('task')
@click.argument('runid')
@click.pass_context
def _task_run_detail(ctx, usecase, task, runid):
    """
    Show detail of a given run
    """

    backend = ctx.obj['backend']
    result = backend.task_run_detail(usecase, task, runid)

    status = result['status']
    if status in ['failure', 'error']:
        print("Failure while accessing backend")
        if 'error' in result:
            print("Reason:", result['error'])
        return


    sdkapi.draw_run_detail(backend, 'run-detail', result,
                           {
                               'Usecase': usecase,
                               'Task': task,
                               'RunID': runid
                           })


@click.group()
@click.argument("backend")
@click.argument("service")
@click.pass_context
def featurestore(ctx, backend, service):
    """
    Access featurestore at backend
    """
    try:
        filename = ctx.obj['config']
        config = json.load(open(filename))
    except:
        traceback.print_exc()
        raise Exception("Invalid config file: {}".format(ctx.obj['config']))

    backends = config['backends']

    relevant = None
    for b in backends:
        if ((b.get('server',None) == backend) or
            (b.get('name',None) == backend)):
            relevant = b
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))

    # Decode the key before accessing
    key = base64.b64decode(relevant['key'].encode('utf-8')).decode('utf-8')
    relevant['key'] = key

    backend = sdkapi.Backend(relevant)
    ctx.obj['backend'] = backend

    # Lookup the service as well..
    services = config['services']
    relevant = None
    for s in services:
        if s.get('name',None) == service:
            relevant = s
            break

    if relevant is None:
        raise Exception("Invalid backend name: {}".format(name))
    ctx.obj['service'] = s

@featurestore.command("post")
@click.argument('filename')
@click.option("--debug/--no-debug",
              default=False)
@click.pass_context
def _post(ctx, filename, debug,):
    """
    Post json to server
    """

    backend = ctx.obj['backend']
    service = ctx.obj['service']

    response = fslib.post(backend=backend,
                          service=service,
                          filename=filename,
                          debug=debug)
    print(response)

@featurestore.command("generate")
@click.option("--debug/--no-debug",
              default=False)
@click.pass_context
def _generate(ctx, debug):
    """
    Generate sample files
    """

    backend = ctx.obj['backend']
    service = ctx.obj['service']

    response = fslib.generate(backend=backend,
                              service=service,
                              debug=debug)
    print(json.dumps(response, indent=4))

@featurestore.command("download")
@click.option('--featuregroup_id', default=None)
@click.option('--run_id', default=None)
@click.option("--debug/--no-debug",  default=False)
@click.pass_context
def _spec_download(ctx, featuregroup_id, run_id, debug,):
    """
    Download a featuregroup specification
    """

    if featuregroup_id is None and run_id is None:
        raise Exception("One of the featuregroup_id or run_id should be specified")

    backend = ctx.obj['backend']
    service = ctx.obj['service']

    response = fslib.download(backend=backend,
                              service=service,
                              featuregroup_id=featuregroup_id,
                              run_id=run_id,
                              debug=debug)
    print(json.dumps(response, indent=4))


@featurestore.command("search", context_settings=dict(
    ignore_unknown_options=True,
))
@click.option("--debug/--no-debug",  default=False)
@click.argument('params', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def _spec_search(ctx, debug, params):
    """
    Search for a feature spec or run
    """

    backend = ctx.obj['backend']
    service = ctx.obj['service']

    def error():
        print("Args should have attr=value format")
        print("Example: ....local spec search name=customer_persona")
        print("You can give django filter query name__icontains=persona")
        return

    for p in params:
        if p.count("=") != 1:
            return error()

    params = { p.split("=")[0]: p.split("=")[1] for p in params}
    if len(params) == 0:
        return error()

    response = fslib.search(backend=backend,
                            service=service,
                            params=params,
                            debug=debug)

    print(json.dumps(response, indent=4))

api.add_command(config)
api.add_command(show)
api.add_command(featurestore)

###################################
# Add to process
###################################
process.add_command(_version)
process.add_command(_start)
process.add_command(bootstrap_)
process.add_command(envsetup)
process.add_command(api)
process.add_command(test)
process.add_command(_show_log)

def main():
    process()


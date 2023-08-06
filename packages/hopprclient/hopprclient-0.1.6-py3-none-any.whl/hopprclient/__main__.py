#!/usr/bin/python

import os, sys, getopt, json
from . import service_clients
from . import hoppr_client

def main():
    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv,'hacdFf:e:s:w:', ['help', 'configure-auth', 'configure-client-id', 'configure-dataset', 'force-upload', 'folder=', 'env=', 'batch-size=', 'batch-wait='])
    except getopt.GetoptError:
        print('Usage: python -m hopprclient -f <folder>')
        sys.exit(2)

    folder = None
    env = 'prd'
    configure_auth = False
    configure_client_id = False
    configure_dataset = False
    force_upload = False
    batch_size = None
    batch_wait = None
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('To use hopprclient, you must specify a folder to scan for files to upload.')
            print('python -m hopprclient -f <folder>')
            print()
            print('Please see the README for an explanation of all command line arguments.')
            sys.exit()
        elif opt in ('-f', '--folder'):
            folder = os.path.abspath(arg)
        elif opt in ('-e', '--env'):
            print('Targeting ' + arg + ' environment.')
            env = arg
        elif opt in ('-a', '--configure-auth'):
            configure_auth = True
        elif opt in ('-c', '--configure-client-id'):
            configure_client_id = True
        elif opt in ('-d', '--configure-dataset'):
            configure_dataset = True
        elif opt in ('-F', '--force-upload'):
            force_upload = True
        elif opt in ('-s', '--batch-size'):
            batch_size = int(arg)
        elif opt in ('-w', '--batch-wait'):
            batch_wait = float(arg)

    base_url = 'https://api-' + env + '.hoppr.ai'
    
    script_path = os.path.abspath(os.path.dirname(__file__))
    app_config_path = os.path.join(script_path, '.hoppr')

    if not os.path.isdir(app_config_path):
        os.mkdir(app_config_path)

    app_config_file = os.path.join(app_config_path, 'config.json')
    app_config = {}
    credentials = None
    client_id = None
    try:
        with open(app_config_file) as f:
            app_config = json.load(f)
            credentials = app_config['credentials']
            if credentials is not None:
                print('Credentials loaded from config file.')
                print('To reset the credentials, run the program with the -a (--configure-auth) argument.')
            client_id = app_config['clientId']
            if client_id is not None:
                print('Client ID used to hash PII loaded from config file.')
                print('To reset the client ID used for hashing, run the program with the -c (--configure-client-id) argument.')
    except IOError:
        pass

    if credentials is None or configure_auth:
        credentials = {}
        print('Configuring credentials. Please enter your credentials at the prompt.')
        credentials['Hoppr-Account-Id'] = input('Account ID: ')
        credentials['Hoppr-Account-Secret'] = input('Account Secret: ')
        app_config['credentials'] = credentials

        with open(app_config_file, 'w') as f:
            json.dump(app_config, f, indent=2)

    if client_id is None or configure_client_id:
        print('Configuring client ID for hashing PII. Please enter your client ID at the prompt.')
        client_id = input('Client ID: ')
        app_config['clientId'] = client_id

        with open(app_config_file, 'w') as f:
            json.dump(app_config, f, indent=2)
        
    if folder is None:
        print('No folder passed to process, exiting.')
        print('Usage: python -m hopprclient -f <folder>')
        sys.exit()

    if not os.path.isdir(folder):
        print('Invalid folder passed to process, exiting.')
        sys.exit()

    # Service clients
    http_client = service_clients.http_service_client.HttpServiceClient(base_url, credentials)
    files_client = service_clients.files_service_client.FilesServiceClient(http_client)

    client = hoppr_client.HopprClient(files_client)

    client.process(folder, configure_dataset, batch_size, batch_wait, force_upload)

if __name__ == '__main__':
    main()
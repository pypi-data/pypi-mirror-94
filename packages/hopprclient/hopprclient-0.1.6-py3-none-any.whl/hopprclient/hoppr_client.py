import os, sys, json, hashlib, datetime, time

class HopprClient:
    BLOCKED_FOLDER_PREFIXES = ['.', '__MACOSX']
    MAX_FILE_SIZE_BYTES = 5000000000 # 5 GB

    def __init__(self, files_service_client):
        self._files_service_client = files_service_client
    
    def process(self, folder, configure_dataset, batch_size, batch_wait, force_upload):
        os.chdir(folder)

        config_folder = '.hoppr'
        if not os.path.isdir(config_folder):
            os.mkdir(config_folder)

        dataset_config_file = os.path.join(config_folder, 'config.json')
        dataset_config = {}
        dataset_id = None
        dataset = None
        try:
            with open(dataset_config_file) as f:
                dataset_config = json.load(f)
                dataset_id = dataset_config['datasetId']
                if dataset_id is not None:
                    dataset = self._files_service_client.get_dataset(dataset_id)
                    if dataset is None:
                        print('Loaded dataset config from file, but the dataset does not exist.')
                        print('Clearing config setting.')
                        dataset_id = None
                    else:
                        print('Dataset loaded from config file.')
                        print('To reset the dataset for this folder, run the program with the -d (--configure-dataset) argument.')
            
                if 'batchSize' in dataset_config and batch_size is None:
                    batch_size = dataset_config['batchSize']
                if 'batchWait' in dataset_config and batch_wait is None:
                    batch_wait = dataset_config['batchWait']
        except IOError:
            pass

        if dataset_id is None or configure_dataset:
            dataset = self._get_dataset(folder)
            dataset_config['datasetId'] = dataset['id']
        
        if batch_size is None:
            batch_size = 50
        else:
            dataset_config['batchSize'] = batch_size
        if batch_wait is None:
            batch_wait = 0.5
        else:
            dataset_config['batchWait'] = batch_wait

        with open(dataset_config_file, 'w') as f:
            json.dump(dataset_config, f, indent=2)
        
        self._process_folder(folder, '/', batch_size, batch_wait, dataset_config_file, dataset_config, force_upload)

    def _get_dataset(self, folder):
        dataset_name = os.path.basename(folder)
        dataset = self._files_service_client.get_dataset_by_name(dataset_name)
        if dataset is None:
            dataset = {}
            dataset['name'] = dataset_name

            dataset = self._files_service_client.create_dataset(dataset)
        
        return dataset

    def _process_folder(self, folder, relative_path, batch_size, batch_wait, dataset_config_file, dataset_config, force_upload):
        files = []
        self._scan_folder(folder, relative_path, files)

        file_count = len(files)
        print('There are {:d} files to be processed.'.format(file_count))

        total_uploaded = 0; total_skipped = 0
        
        uploaded = []
        if 'uploaded' in dataset_config:
            uploaded = dataset_config['uploaded']

        
        uploaded_count = len(uploaded)

        batch = []
        dataset_id = dataset_config['datasetId']

        uploaded_index = 0
        for file_index in range(file_count):
            item = files[file_index]
            path = item['relativePath'] + item['name']
            md5Hash = item['md5Hash']

            while uploaded_index < uploaded_count and uploaded[uploaded_index]['path'] < path:
                # Files were deleted
                del uploaded[uploaded_index]
                uploaded_count -= 1

            already_uploaded = False
            file_same = False
            if uploaded_index < uploaded_count:
                already_uploaded = uploaded[uploaded_index]['path'] == path
                file_same = uploaded[uploaded_index]['md5Hash'] == md5Hash
                if not force_upload and already_uploaded and file_same:
                    # We have already uploaded this file
                    uploaded_index += 1
                    total_skipped += 1
                    continue

            # Place the file in a batch
            batch.append(item)

            if not already_uploaded:
                if uploaded_index < uploaded_count and uploaded[uploaded_index]['path'] > path:
                    uploaded.insert(uploaded_index, {'path': path, 'md5Hash': md5Hash})
                else:
                    uploaded.append({'path': path, 'md5Hash': md5Hash})
                uploaded_count += 1
            elif not file_same and uploaded_index < uploaded_count:
                uploaded[uploaded_index]['md5Hash'] = md5Hash

            uploaded_index += 1
            total_uploaded += 1

            if len(batch) == batch_size:
                # Upload the batch and report progress
                if not self._process_batch(dataset_id, batch):
                    print('Failed to upload batch file(s), exiting.')
                    sys.exit()

                batch = []
                percent_done = (total_uploaded + total_skipped) / file_count * 100
                print('Uploaded: {:d}, Skipped: {:d}, {:3.2f}% done'.format(total_uploaded, total_skipped, percent_done))

                dataset_config['uploaded'] = uploaded
                with open(dataset_config_file, 'w') as f:
                    json.dump(dataset_config, f, indent=2)

                # Sleep between batches
                time.sleep(batch_wait)

        if len(batch) > 0:
            # Upload the final batch  
            if not self._process_batch(dataset_id, batch):
                print('Failed to upload batch file(s), exiting.')
                sys.exit()

            percent_done = (total_uploaded + total_skipped) / file_count * 100
            print('Uploaded: {:d}, Skipped: {:d}, {:3.2f}% done'.format(total_uploaded, total_skipped, percent_done))

        dataset_config['uploaded'] = uploaded
        with open(dataset_config_file, 'w') as f:
            json.dump(dataset_config, f, indent=2)  
        
        print('Dataset upload completed :)')
    
    def _process_batch(self, dataset_id, batch):
        # Compute the client IDs for the files
        for item in batch:
            path = item['relativePath'] + item['name']
            item['hashedId'] = self._compute_url_safe_hash(path, dataset_id)

        file_hashes = self._files_service_client.get_file_hashes([x['hashedId'] for x in batch])
        
        metadata_batch = []

        for item in batch:
            hashed_id = item['hashedId']
            if hashed_id in file_hashes and file_hashes[hashed_id] == item['md5Hash']:
                continue

            file_metadata = {}
            file_metadata['filePath'] = item['relativePath']
            file_metadata['fileName'] = item['name']
            file_metadata['hashedId'] = hashed_id
            file_metadata['datasetId'] = dataset_id
            file_metadata['md5Hash'] = item['md5Hash']
            file_metadata['size'] = item['size']
            utc_now = str(datetime.datetime.utcnow())
            if hashed_id not in file_hashes:
                file_metadata['dateCreated'] = utc_now
            file_metadata['dateUpdated'] = utc_now

            metadata_batch.append(file_metadata)
        
        metadata_batch_response = self._files_service_client.upload_file_metadata_batch(metadata_batch)

        file_batch = {}

        for item in batch:
            hashed_id = item['hashedId']
            if hashed_id in metadata_batch_response:
                file_batch[item['path']] = metadata_batch_response[hashed_id]
        
        return self._upload_file_batch(file_batch)

    def _upload_file_batch(self, file_batch):
        if len(file_batch) == 0:
            return True

        return self._files_service_client.upload_file_batch(file_batch)
    
    def _scan_folder(self, folder, relative_path, files):
        items = os.listdir(folder)
        for item in items:
            path = os.path.join(folder, item)
            if os.path.isdir(path):
                if all([not item.startswith(prefix) for prefix in self.BLOCKED_FOLDER_PREFIXES]):
                    self._scan_folder(path, relative_path + item + '/', files)

            elif not item.startswith('.'):
                file_size = os.path.getsize(path)
                if file_size > self.MAX_FILE_SIZE_BYTES:
                    print('File ' + path + ' skipped because it was too large.')
                    continue

                dataset_file = {}
                dataset_file['path'] = path
                dataset_file['relativePath'] = relative_path
                dataset_file['name'] = item
                dataset_file['size'] = file_size
                with open(path, 'rb') as f:
                    contents = f.read()
                    dataset_file['md5Hash'] = hashlib.md5(contents).hexdigest()
                
                files.append(dataset_file)
    
    def _compute_url_safe_hash(self, cleartext, salt):
        h = hashlib.sha256(cleartext.encode() + salt.encode()).hexdigest()
        return h.rstrip('=').replace('+', '-').replace('/', '_')
            
        
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import ReceivedFax
import faxbox.settings
import requests
import boto3

import os

@shared_task
def download_media(received_fax: ReceivedFax):
    print('Downloading media url:', received_fax.media_url)
    resp = requests.get(received_fax.media_url)
    try:
        resp.raise_for_status()
        file_id = received_fax.pk
        file_name = '{}.pdf'.format(file_id)
        file_path = os.path.join(faxbox.settings.MEDIA_ROOT, file_name)
        print('Saving file to: ', file_path)
        with open(file_path, 'wb') as f:
            f.write(resp.content)
        print('Uploading to spaces...')
        upload_to_spaces(file_path, file_id)
        print('done')
    except:
        raise

@shared_task
def upload_to_spaces(file_path, file_id):
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name=faxbox.settings.OBJECT_STORE_REGION,
                            endpoint_url=faxbox.settings.OBJECT_STORE_URL,
                            aws_access_key_id=faxbox.settings.OBJECT_STORE_KEY_ID,
                            aws_secret_access_key=faxbox.settings.OBJECT_STORE_KEY_SECRET)

    client.upload_file(file_path, 'veryserious', '{}/fax.pdf'.format(file_id))
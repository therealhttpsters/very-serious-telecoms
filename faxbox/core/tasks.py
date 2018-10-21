from __future__ import absolute_import, unicode_literals
from celery import shared_task
from core.models import ReceivedFax
from faxbox.settings import MEDIA_ROOT
import requests

import os

@shared_task
def download_media(received_fax: ReceivedFax):
    print('Downloading media url:', received_fax.media_url)
    resp = requests.get(received_fax.media_url)
    try:
        resp.raise_for_status()
        file_path = os.path.join(MEDIA_ROOT, '{}.pdf'.format(received_fax.pk))
        print('Saving file to: ', file_path)
        with open(file_path, 'wb') as f:
            f.write(resp.content)
    except:
        raise





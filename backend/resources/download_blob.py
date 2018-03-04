from azure.storage.blob import BlockBlobService
from azure.storage.blob import ContentSettings
from azure.storage.blob import PublicAccess
from variables import blob_account_key
import requests

container_name = 'container0'
blob_name = 'blob0'
video_name = 'video.mp4'

def push(filepath):
	# upload with blob
	# block_blob_service = BlockBlobService(account_name='wordsplitter', account_key=blob_account_key)
	# block_blob_service.create_container(container_name, public_access=PublicAccess.Container)
	# block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
	# block_blob_service.create_blob_from_path(container_name, blob_name, filepath, content_settings=ContentSettings(content_type='video/mp4'))


	# start job with requests

	# delete blob
	#block_blob_service.delete_blob(container_name, blob_name)

def download(container):
	block_blob_service = BlockBlobService(account_name='wordsplitter', account_key=blob_account_key)
	gen = block_blob_service.list_blobs(container)
	blob_name = None
	for blob in gen:
		if blob.name.endswith('.info'):
			blob_name = blob.name
	block_blob_service.get_blob_to_path(container, blob_name, 'transcript.info')

# download('asset-7bc61df8-9a8c-44ff-a267-915391d8177c')
push('/Users/lee/Documents/pprojects/HackTech2018/backend/video.mp4')
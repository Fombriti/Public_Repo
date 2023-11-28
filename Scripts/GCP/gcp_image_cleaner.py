#
#   Script that, given a keyword, searches for images containing that name within GCP and deletes them.
#   Specify project_id, credentials_path, image_name_contains

from google.cloud import compute_v1
from google.oauth2 import service_account
import time

def create_gcp_credentials(credentials_path):
    return service_account.Credentials.from_service_account_file(credentials_path)

def delete_image(client, project_id, image_name):
    print(f"Deleting imagine '{image_name}'")
    operation = client.delete(project=project_id, image=image_name)
    return operation

def wait_for_global_operation(credentials, project_id, operation_name, image_name):
    operation_client = compute_v1.GlobalOperationsClient(credentials=credentials)
    while True:
        result = operation_client.get(project=project_id, operation=operation_name)
        if result.status == compute_v1.Operation.Status.DONE:
            if result.error:
                raise Exception(result.error)
            print(f"Operation completed for image: {image_name}")
            return
        print(f"Wait. Deleting '{image_name}' now..")
        time.sleep(5)

def list_and_delete_images(credentials, project_id, image_name_contains):
    image_client = compute_v1.ImagesClient(credentials=credentials)
    request = compute_v1.ListImagesRequest(project=project_id)

    found_images = False
    for image in image_client.list(request=request):
        if image_name_contains in image.name:
            found_images = True
            print(f"Image to delete finded: {image.name}")
            operation = delete_image(image_client, project_id, image.name)
            wait_for_global_operation(credentials, project_id, operation.name, image.name)

    if not found_images:
        print(f"No image found containing '{image_name_contains}'.")


# Parameter
project_id = "YOUR_PROJECT_ID"
credentials_path = "YOUR_JSON_CREDENTIAL_PATH"
image_name_contains = "WHAT_TO_FIND_IN_IMAGE_TITLE"

# Script execution
credentials = create_gcp_credentials(credentials_path)
list_and_delete_images(credentials, project_id, image_name_contains)

from google.cloud import storage

PROJECT_ID = "zinc-presence-451322-t0"
GCS_BUCKET = "zinc-presence-451322-bucket1"

def list_buckets():
    """List all buckets"""
    storage_client = storage.Client(project=PROJECT_ID)
    buckets = storage_client.list_buckets()

    for bucket in buckets:
        print(bucket.name)


def create_bucket_class_location(bucket_name):

    bucketName = bucket_name

    storage_client = storage.Client(project=PROJECT_ID)

    bucket = storage_client.bucket(bucket_name=bucketName)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="europe-west2")

    print(
        "Created bucket {} in {} with storage classs {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )

    return new_bucket



def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client(project=PROJECT_ID)

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    # Note: The call returns a response only when the iterator is consumed.
    for blob in blobs:
        print(blob.name)




def upload_blob(bucket_name, file_to_upload, blob_name_destination):

    # The ID of your GCS bucket
    bucketName = bucket_name

    # The path to your file to upload
    source_file = file_to_upload

    # The ID of your GCS object
    destination_blob_name = blob_name_destination


    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(bucketName)
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    blob.upload_from_filename(source_file, if_generation_match=generation_match_precondition)

    print(
        f"File {source_file} uploaded to {destination_blob_name}"
    )

    print("Listing the contents inside this bucket: ", list_blobs(bucket_name))

# upload_blob(GCS_BUCKET, "decentralized_employee_data.xlsx", "employee-data-demo-sheet")

list_blobs(GCS_BUCKET)
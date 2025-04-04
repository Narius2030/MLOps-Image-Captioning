from pyspark.sql.types import StringType, StructType, StructField

image_schema = StructType([
    StructField("image_name", StringType(), False),
    StructField("image_base64", StringType(), False),
    StructField("image_size", StringType(), True)
])


csv_schema = StructType([
    StructField("original_url", StringType(), False),
    StructField("source_website", StringType(), True),
    StructField("resolution", StringType(), True),
    StructField("search_query", StringType(), True),
    StructField("local_path", StringType(), True),
    StructField("caption", StringType(), False)
])

minio_schema = """
{
    "EventName": "s3:ObjectCreated:Put",
    "Key": "lakehouse/imcp/parquets/customer.csv",
    "Records": [
        {
            "eventVersion": "2.0",
            "eventSource": "minio:s3",
            "awsRegion": "",
            "eventTime": "2025-02-01T06:12:38.009Z",
            "eventName": "s3:ObjectCreated:Put",
            "userIdentity": {
                "principalId": "minio"
            },
            "requestParameters": {
                "principalId": "minio",
                "region": "",
                "sourceIPAddress": "27.2.17.171"
            },
            "responseElements": {
                "x-amz-id-2": "dd9025bab4ad464b049177c95eb6ebf374d3b3fd1af9251148b658df7ac2e3e8",
                "x-amz-request-id": "182000D1F6E072E7",
                "x-minio-deployment-id": "4b824120-0a08-42ac-9dd7-10dc4c3b6903",
                "x-minio-origin-endpoint": "http://172.19.0.4:9000"
            },
            "s3": {
                "s3SchemaVersion": "1.0",
                "configurationId": "Config",
                "bucket": {
                    "name": "lakehouse",
                    "ownerIdentity": {
                        "principalId": "minio"
                    },
                    "arn": "arn:aws:s3:::lakehouse"
                },
                "object": {
                    "key": "imcp%2Fparquets%2Fcustomer.csv",
                    "size": 64509,
                    "eTag": "0af67f9a60ad0f49ecdb1b3e8ac988d0",
                    "contentType": "text/csv",
                    "userMetadata": {
                        "content-type": "text/csv"
                    },
                    "versionId": "6f53c1c4-b3e4-4b01-9eb0-49aa432b3a58",
                    "sequencer": "182000D1FA020CBF"
                }
            },
            "source": {
                "host": "27.2.17.171",
                "port": "",
                "userAgent": "MinIO (linux; amd64) minio-go/v7.0.82 MinIO Console/(dev)"
            }
        }
    ]
}
"""
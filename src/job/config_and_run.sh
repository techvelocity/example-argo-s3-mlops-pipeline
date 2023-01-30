#!/bin/sh
sed -i 's/aws-access-key-id/'$AWS_ACCESS_KEY_ID'/g' s3-workflow.yaml
sed -i 's|aws-secret-access-key|'$AWS_SECRET_ACCESS_KEY'|g' s3-workflow.yaml
sed -i 's|s3-raw-images|'$S3_RAW_IMAGES'|g' s3-workflow.yaml
sed -i 's/s3-processed-images/'$S3_PROCESSED_IMAGES'/g' s3-workflow.yaml

python main.py
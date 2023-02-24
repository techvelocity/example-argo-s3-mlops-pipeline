#!/bin/sh
sed -i 's/aws-access-key-id/'$AWS_ACCESS_KEY_ID'/g' s3-workflow.yaml
sed -i 's|aws-secret-access-key|'$AWS_SECRET_ACCESS_KEY'|g' s3-workflow.yaml
sed -i 's|s3-name|'$S3_NAME'|g' s3-workflow.yaml

python main.py
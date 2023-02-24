import os
import boto3
import torch
from torchvision import transforms
from PIL import Image
from io import BytesIO

class PrepImages:
    def __init__(self):
        self.bucket_name = os.environ.get('S3_NAME')
        self.s3_client = boto3.client('s3')
        self.raw_images = []
        self.processed_images = []

    def download_from_s3(self):
        paginator = self.s3_client.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=self.bucket_name)
        for page in result:
            for item in page['Contents']:
                obj = self.s3_client.get_object(
                    Bucket=self.bucket_name,
                    Key=item['Key'])
                data = {'filename':item['Key'], 'data': obj}
                image_name = data['filename'].split('.')
                ext = image_name[1]
                if ext != 'pt':
                    self.raw_images.append(data)

    def process_images(self):
        imagenet_mean = [0.485, 0.456, 0.406]
        imagenet_std = [0.229, 0.224, 0.225]
        t = transforms.Compose(
            [transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=imagenet_mean, std=imagenet_std)]
        )
        for item in self.raw_images:
            image_name = item['filename'].split('.')[0]
            file = bytes(item['data']['Body'].read())
            metadata = item['data']['Metadata']
            processed_image = {}
            processed_image['name'] = f"{image_name}.pt"
            processed_image['metadata'] = metadata
            img_pil = Image.open(BytesIO(file)).convert('RGB')
            img_tensor = t(img_pil)
            img_tensor = torch.unsqueeze(img_tensor, 0)
            torch.save(img_tensor, processed_image['name'])
            self.processed_images.append(processed_image)

    def upload_to_s3(self):
        for item in self.processed_images:
            with open(item['name'], 'rb') as f:
                self.s3_client.put_object(
                    Body=f, 
                    Bucket=self.bucket_name, 
                    Key=item['name'], 
                    Metadata=item['metadata'])

    def remove_from_bucket(self):
        for item in self.raw_images:
            image_name = item['filename'].split('.')
            ext = image_name[1]
            image_name = image_name[0]
            if ext != 'pt':
                self.s3_client.delete_object(
                    Bucket=self.bucket_name,
                    Key=item['filename']
                )

def main():
    prep_images = PrepImages()
    prep_images.download_from_s3()
    if len(prep_images.raw_images) > 0:
        prep_images.process_images()
        prep_images.upload_to_s3()
        prep_images.remove_from_bucket()

if __name__ == "__main__":
    main()

import os
import boto3
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import  HTMLResponse


app = FastAPI()

S3_NAME = os.environ.get('S3_NAME')

@app.get('/')
async def index_view():
    return HTMLResponse("""
        <div style="background-color: #707aaa; margin: 15px; border-radius: 5px; padding: 15px; width: 300px">
        <b>Upload an image: </b>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <p><input type=file name=file value="Pick an image">
            <p><input type=text name=label value="Label image">
            <p><input type=submit value="Upload">
        </form>
        </div>""")

@app.post('/upload')
async def upload_image(label: str = Form(), file: UploadFile = File(...)):
    metadata = {'label': label}
    s3_client = boto3.client('s3')
    s3_client.put_object(
        Body=file.file, 
        Bucket=S3_NAME, 
        Key=str(file.filename), 
        Metadata=metadata)
    return HTMLResponse("""
        <div style="background-color: #707aaa; margin: 15px; border-radius: 5px; padding: 15px; width: 300px">
        <b>Upload an image: </b>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <p><input type=file name=file value="Pick an image">
            <p><input type=text name=label value="Label image">
            <p><input type=submit value="Upload">
        </form>
        </div>""")

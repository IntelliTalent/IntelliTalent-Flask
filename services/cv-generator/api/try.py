import requests

url = f"http://localhost:3000/api/v1/uploader/upload"
file_path = "generated-cvs/waer-alwaer-10-05-2024,18-38-58.docx"
filename = file_path.split('/')[-1]

payload = {}
files=[
    (
        'file',
        (
            filename,
            open(file_path,'rb')
        )
    )
]

headers = {}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

print(response.text)
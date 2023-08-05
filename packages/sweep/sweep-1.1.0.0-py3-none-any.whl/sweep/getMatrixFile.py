import requests
from tqdm import tqdm
import hashlib
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
    total_size = int(response.headers.get('content-length', 0))
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    chunk_size = 32768
    print('The download destination is <'+destination+'>.\nDownloading 739MiB...', flush=True)
    t=tqdm(total=total_size, unit='iB', unit_scale=True, position=0, leave=True)
    with open(destination, "wb") as f:
        for chunk in response.iter_content(chunk_size):
            t.update(len(chunk))
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR, something went wrong!", flush=True)
def getMatrixFile(file):
    try:
        if md5(file) != 'f18587ac79c452e419f0bcb2059d6619':
            print('Something wrong with default matrix file...', flush=True)
            download_file_from_google_drive('1po8LSbM1jrxUGdICGrvrejaZtFtyCE1y',file)
    except:
        print('Default matrix file not found...', flush=True)
        download_file_from_google_drive('1po8LSbM1jrxUGdICGrvrejaZtFtyCE1y',file)
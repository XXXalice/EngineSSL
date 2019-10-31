from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import glob
from tqdm import tqdm

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

models = glob.glob("*.h5")
print(models)
for model in tqdm(models):
    f = drive.CreateFile({"title": model})
    f.SetContentFile(model)
    f.Upload()
import requests
url = "https://drive.google.com/file/d/1gjPVAbybIv3xS8MsxsKoFoxhkIgPQRbQ/view?usp=sharing"
r = requests.get(url)
with open("model.pkl", "wb") as f:
    f.write(r.content)



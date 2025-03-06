# 🚚 Camionnette365

Camionnette365 is a tool designed to attempt extracting Office 365 data through a phishing application on IntraID.

![camionnette](./static/img.png)

> ⚠️ **Warning :** Juste education purpose it's méchant of not be gentil
> 

---

## Roadmap

- [x] Add oneNote dump
- [x] Add oneDrive dump
- [ ] Add exchange dump
---

## Setup

### IntraId setup

#### With az

```
APP_ID=$(az ad app create --display-name "Camionnette365" | jq -r ".appId")
az ad app update --id "$APP_ID" --web-redirect-uris "https://camionnette365.kleman.pw/getAToken"
az ad app credential reset --id $APP_ID --append --years 1
az ad app update --id "$APP_ID" --set signInAudience="AzureADMultipleOrgs" # for multi tenant app
```

#### With GUI

- Go to https://entra.microsoft.com, navigate to Identity > Applications > Register applications.
- Register a new application.
- Configure the Redirection URI to match your website URL in the application settings.


### Website Setup

Set up `.env` and `app.py`.

#### Venv

```bash
python3 -m venv . 
source ./bin/activate
python3 app.py
```

#### Docker

```bash
docker build -t camionnette365 .
docker run -d --rm -p 8000:8000 -v $(pwd)/data:/app/data camionnette365
```


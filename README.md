
# CSV to JSON converter

This was made for two API and Web Services assignments at UTFPR, Toledo, Parana, Brazil.

## How to use 
clone this repo
python3 main.py {file.csv} {file.json}

## Comments on the code and clutter
You will notice a lot of clutter on the code, that is due to time constraints.


## How to use
change these to the column titles in the csv file
```
local = {
 92                 "cedente": get("cedente"),
 93                 "pagador": get("pagador"),
 94                 "valor": get("valor"),
 95                 "logradouro": get(""),
 96                 "numero": parse_int(get("valor"), default=0),
 97             }


135                 "cedente": local.get("cedente", ""),
136                 "pagador": local.get("pagador", ""),
137                 "valor": local.get("valor", ""),
138                 "vencimento": data_str,  # dd/MM/yyyy
```
## Project running
![WhatsApp Image 2025-11-27 at 16 28 43](https://github.com/user-attachments/assets/20a2f2fd-eb55-4f98-a74f-caefcd53360b)

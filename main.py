#!/usr/bin/env python3
"""
Lê 'furtos.csv' e gera 'furtos.json' com documentos achatados.
Gera _id no formato ObjectId (Extended JSON: {"$oid":"<24hex>"}).
Formato da data em dataOcorrencia: dd/MM/yyyy.

Uso:
  # usa arquivos padrão
  python carregar_boletins.py

  # ou especificar input e output
  python carregar_boletins.py input.csv output.json
"""
from typing import List, Dict, Any
import csv
import json
import sys
from datetime import datetime
from pathlib import Path
import secrets

CSV_DATE_FORMAT = "%d/%m/%Y"  # formato de entrada e saída desejado

# string de classe fornecida pelo usuário
DEFAULT_CLASS = "com.br.td.utfpr.edu.tsi.cadastro_usuarios.model"


# tenta usar bson.ObjectId se disponível, senão gera 24 hex aleatório
def make_objectid_hex() -> str:
    try:
        # pymongo/bson fornece ObjectId
        from bson.objectid import ObjectId  # type: ignore

        return str(ObjectId())
    except Exception:
        # fallback: 12 bytes -> 24 hex chars
        return secrets.token_hex(12)


def parse_int(value: str, default: int = 0) -> int:
    try:
        value = (value or "").strip()
        return int(value) if value != "" else default
    except Exception:
        return default


def parse_date_ddmmyyyy(value: str) -> str:
    """
    Converte data do CSV (esperada em dd/MM/yyyy) para string no mesmo formato.
    Se valor inválido ou ausente, retorna string vazia.
    """
    value = (value or "").strip()
    if not value:
        return ""
    try:
        d = datetime.strptime(value, CSV_DATE_FORMAT).date()
        return d.strftime(CSV_DATE_FORMAT)  # "dd/MM/yyyy"
    except Exception:
        return ""


def carregar(caminho_csv: str, class_name: str = DEFAULT_CLASS) -> List[Dict[str, Any]]:
    """
    Lê o CSV (tenta detectar delimitador; padrão tab se não detectado) e retorna
    uma lista de documentos achatados no formato solicitado, com _id gerado.
    """
    boletins: List[Dict[str, Any]] = []
    path = Path(caminho_csv)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_csv}")

    with path.open(newline="", encoding="utf-8") as f:
        sample = f.read(2048)
        f.seek(0)
        delimiter = "\t"
        try:
            sniffed = csv.Sniffer().sniff(sample, delimiters=[",", ";", "\t", "|"])
            delimiter = sniffed.delimiter
        except Exception:
            delimiter = "\t"

        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            get = lambda k: (row.get(k) or "").strip()

          #  id_boletim = get("cnodigo")
            data_str = parse_date_ddmmyyyy(get("vencimento"))
          #  periodo = get("cedente")

            local = {
                "cedente": get("cedente"),
                "pagador": get("pagador"),
                "valor": get("valor"),
                "logradouro": get(""),
                "numero": parse_int(get("valor"), default=0),
            }

          #  emplacamento = {
          #      "cidade": get("CIDADE_VEICULO"),
          #      "estado": get("UF_VEICULO"),
          #      "placa": get("PLACA_VEICULO"),
          #  }

          #  veiculo = {
          #      "emplacamento": emplacamento,
          #      "cor": get("DESCR_COR_VEICULO"),
          #      "tipoVeiculo": get("DESkCR_TIPO_VEICULO"),
          #      "marca": get("DESCR_MARCA_VEICULO"),
          #  }

          #  ano_fab = get("ANO_FABRICACAO")
          #  ano_mod = get("ANO_MODELO")
          #  if ano_fab != "":
          #      veiculo["anoFabricacao"] = parse_int(ano_fab, default=0)
          #  elif ano_mod != "":
          #      veiculo["anoFabricacao"] = parse_int(ano_mod, default=0)
          #  else:
          #      veiculo["anoFabricacao"] = 0

          #  parte = {"tipoEnvolvimento": get("TIPOPESSOA")}

            # Gera ObjectId hex (24 chars). Usamos Extended JSON format {"$oid": "<hex>"}
            oid_hex = make_objectid_hex()
            doc: Dict[str, Any] = {
               # "_id": {"$oid": oid_hex},
                # se houver colunas NOME/EMAIL/IDADE no CSV, usamos; senão vazio
               # "nome": get("NOME") if "NOME" in row else "",
               # "email": get("EMAIL") if "EMAIL" in row else "",
               # "idade": get("IDADE") if "IDADE" in row else "",
               # "envolvimento": parte.get("tipoEnvolvimento", ""),
               # "veiculo": veiculo.get("marca", ""),
               # "emplacamento": emplacamento.get("placa", ""),
               # "logradouroOcorrencia": local.get("logradouro", ""),
                "cedente": local.get("cedente", ""),
                "pagador": local.get("pagador", ""),
                "valor": local.get("valor", ""),
                "vencimento": data_str,  # dd/MM/yyyy ou "" se ausente
               # "_class": class_name,
                # mantemos referência ao número original do boletim (se precisar)
               # "numeroBoletimOriginal": id_boletim or "",
                # opcional: manter estrutura aninhada dentro do documento
                # "original": {
                #     "periodoOcorrencia": periodo,
                #     "localOcorrencia": local,
                #     "veiculoFurtado": veiculo,
                #     "parte": parte
                # }
            }

            boletins.append(doc)

    print(f"Extração CSV concluída ({len(boletins)} registros).")
    return boletins


def carregar_json(lista: List[Dict[str, Any]], output: str) -> None:
    with open(output, "w", encoding="utf-8") as f:
        json.dump(lista, f, ensure_ascii=False, indent=2)
    print(f"Carregamento JSON concluído -> {output}")


def main(argv):
    # Defaults: input 'furtos.csv', output 'furtos.json'
    if len(argv) == 1:
        input_csv = "furtos.csv"
        output_json = "furtos.json"
    elif len(argv) == 3:
        input_csv = argv[1]
        output_json = argv[2]
    elif len(argv) == 4:
        # permitir passar também a string _class como terceiro argumento
        input_csv = argv[1]
        output_json = argv[2]
        class_name = argv[3]
    else:
        print("Uso: python carregar_boletins.py [input.csv output.json [class_name]]")
        print("Se não informado usa: input='furtos.csv' output='furtos.json'")
        return 1

    # se class_name não veio via argv, usa a DEFAULT_CLASS
    class_name = locals().get("class_name", DEFAULT_CLASS)

    try:
        lista = carregar(input_csv, class_name=class_name)
        carregar_json(lista, output_json)
    except FileNotFoundError as e:
        print(e)
        return 2
    except Exception as e:
        print("Erro:", e)
        return 3

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

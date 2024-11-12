import requests
import time

time_delay = 0.02


def search_keyword_juso_kakao(query, api_key):
    endpoint = "https://dapi.kakao.com/v2/local/search/keyword.json"

    headers = {"Authorization": "KakaoAK " + api_key}
    data = {"query": query, "analyze_type": "simiar"}

    response = requests.get(endpoint, headers=headers, params=data)

    json = response.json()

    if "documents" not in json:
        return None

    documents = json["documents"]

    if len(documents) == 0:
        return None

    return documents[0]


def search_juso_naver(query, client_id, client_key):
    endpoint = "https://openapi.naver.com/v1/search/local.json"

    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_key,
    }

    data = {"query": query}

    response = requests.get(endpoint, headers=headers, params=data)

    json = response.json()

    if "items" not in json:
        return None

    items = json["items"]

    if (len(items)) == 0:
        return None

    time.sleep(time_delay)
    return items[0]


def convert_naver_to_kakao(address_item):
    new_address_item = {}
    new_address_item["address_name"] = address_item["address"]
    new_address_item["road_address_name"] = address_item["roadAddress"]
    new_address_item["place_name"] = address_item["title"]
    new_address_item["category_name"] = address_item["category"]

    # remove <b> tags
    new_address_item["place_name"] = (
        new_address_item["place_name"].replace("<b>", "").replace("</b>", "")
    )
    return new_address_item


def search_exact_juso(query, api_key):

    endpoint = "https://dapi.kakao.com/v2/local/search/address.json"

    headers = {"Authorization": "KakaoAK " + api_key}
    data = {"query": query, "analyze_type": "exact"}

    response = requests.get(endpoint, headers=headers, params=data)

    json = response.json()
    if "documents" not in json:
        return None

    documents = json["documents"]

    if len(documents) == 0:
        return None

    time.sleep(time_delay)
    return documents[0]


def search_juso(query, secrets):
    kakao_result = search_keyword_juso_kakao(query, secrets["kakao_api_key"])

    naver_result = None
    if kakao_result is None:
        naver_result = search_juso_naver(
            query, secrets["naver_api_client_id"], secrets["naver_api_key"]
        )

    if kakao_result is None and naver_result is None:
        return {
            "query": query,
            "code_address": "",
            "b_code": "",
            "h_code": "",
        }

    valid_result = kakao_result
    if naver_result is not None:
        valid_result = convert_naver_to_kakao(naver_result)

    valid_address = valid_result["road_address_name"]

    exact_result = search_exact_juso(valid_address, secrets["kakao_api_key"])

    if exact_result is None:
        return {
            "query": query,
            "code_address": valid_address,
            "b_code": "",
            "h_code": "",
        }

    exact_address = exact_result["address"]

    code_address = exact_address["address_name"]
    b_code = exact_address["b_code"]
    h_code = exact_address["h_code"]

    return {
        "query": query,
        "code_address": code_address,
        "b_code": b_code,
        "h_code": h_code,
    }


def main(secrets):
    with open("input.txt", "r") as f:
        addresses = f.readlines()

    addresses = [address.strip() for address in addresses]

    jusos = []
    count = 0
    total = len(addresses)
    for address in addresses:
        count += 1
        print("searching for {} ({}/{})".format(address, count, total))
        juso = search_juso(address, secrets)
        jusos.append(juso)

    with open("output.txt", "w") as f:
        f.write("query,code_address,b_code,h_code\n")
        for juso in jusos:
            f.write(
                "{};{};{};{}\n".format(
                    juso["query"], juso["code_address"], juso["b_code"], juso["h_code"]
                )
            )


def load_secrets():
    with open("secrets.txt", "r") as f:
        secrets = f.readlines()
    secrets = [secret.strip() for secret in secrets]
    secrets = {
        k.strip(): v.strip() for k, v in [secret.split("=") for secret in secrets]
    }
    return secrets


if __name__ == "__main__":
    secrets = load_secrets()
    main(secrets)

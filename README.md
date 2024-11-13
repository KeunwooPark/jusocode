# jusocode

행정동과 법정동 코드를 검색해 주는 스크립트 입니다.

## 사용 방법

1. 패키지를 설치 합니다.

```sh
> pip install -r requirements.txt
```

2. `secrets.txt` 파일을 다음과 같이 구성 합니다.

```txt
kakao_api_key={kakao_api_key}
naver_api_client_id={naver_api_client_id}
naver_api_key={naver_api_key}
```

3. 다음과 같이 `input.txt` 파일을 구성 합니다. 한 줄에 주소가 하나씩만 들어 가면 됩니다.

```txt
대한민국 서울특별시 종로구 청와대로 1
서울 종로구 효자로 12
...
```

4. 스크립트를 실행 합니다.

```sh
> python juso_code.py
```

5. `output.txt`를 확인 합니다. 구분자는 세미콜론 (`;`) 입니다.

## 동작 방식

주소의 이름이 정확하지 않더라도 정확한 키워드 검색으로 정확한 주소를 찾아내고 이에 대한 행정동과 법정동 코드를 검색 합니다.
카카오 api를 통해서 먼저 정확한 주소 검색을 시도 합니다. 만약 카카오 api에서 검색이 안되면 네이버 api를 사용합니다.
이렇게 해서 검색이 된 주소를 다시 카카오 api를 통해서 행정동과 법정동 코드 검색을 시도 합니다.

검색이 되지 않는 주소의 경우 빈 데이터를 출력 합니다.

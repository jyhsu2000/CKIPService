# CKIP Service

[![Docker Hub](https://img.shields.io/badge/Docker_Hub-blue)](https://hub.docker.com/r/jyhsu/ckip-service)

Web service for [ckiplab/ckiptagger](https://github.com/ckiplab/ckiptagger)

## Preparation

- [Download model files](https://github.com/ckiplab/ckiptagger#1-download-model-files) and put into `data` folder

## Start service

1. Start the service using `docker-compose`
    ```
    docker-compose up -d
    ```
   If you want to rebuild the image, add `--build` flag when startup
    ```
    docker-compose up --build -d
    ```
2. Service is now on port `5005`

## Stop service

1. Stop the service using `docker-compose`
    ```
    docker-compose down
    ```

## Endpoint

- Main
    - method: `POST`
    - route: `/`
    - parameter
        - `sentence_list`: sentence list for CKIP tagging, split multiple sentences by linebreak(`\n`)

## Test CKIP Tagger

1. Send request using curl
    ``` bash
    curl -X POST localhost:5005 -F $'sentence_list=土地公有政策?？還是土地婆有政策。.\n最多容納59,000個人,或5.9萬人,再多就不行了.這是環評的結論.'
    ```
2. Get the response like the following one
    <details>
    <summary>JSON Response</summary>

    ```json
    {
        "sentences": [
            {
                "segments": [
                    {
                        "word": "土地公有",
                        "pos": "VH"
                    },
                    {
                        "word": "政策",
                        "pos": "Na"
                    },
                    {
                        "word": "?",
                        "pos": "QUESTIONCATEGORY"
                    },
                    {
                        "word": "？",
                        "pos": "QUESTIONCATEGORY"
                    },
                    {
                        "word": "還是",
                        "pos": "Caa"
                    },
                    {
                        "word": "土地",
                        "pos": "Na"
                    },
                    {
                        "word": "婆",
                        "pos": "Na"
                    },
                    {
                        "word": "有",
                        "pos": "V_2"
                    },
                    {
                        "word": "政策",
                        "pos": "Na"
                    },
                    {
                        "word": "。",
                        "pos": "PERIODCATEGORY"
                    },
                    {
                        "word": ".\\n",
                        "pos": "FW"
                    },
                    {
                        "word": "最多",
                        "pos": "Da"
                    },
                    {
                        "word": "容納",
                        "pos": "VJ"
                    },
                    {
                        "word": "59,000",
                        "pos": "Neu"
                    },
                    {
                        "word": "個",
                        "pos": "Nf"
                    },
                    {
                        "word": "人",
                        "pos": "Na"
                    },
                    {
                        "word": ",",
                        "pos": "COMMACATEGORY"
                    },
                    {
                        "word": "或",
                        "pos": "Caa"
                    },
                    {
                        "word": "5.9萬",
                        "pos": "Neu"
                    },
                    {
                        "word": "人",
                        "pos": "Na"
                    },
                    {
                        "word": ",",
                        "pos": "COMMACATEGORY"
                    },
                    {
                        "word": "再",
                        "pos": "D"
                    },
                    {
                        "word": "多",
                        "pos": "D"
                    },
                    {
                        "word": "就",
                        "pos": "D"
                    },
                    {
                        "word": "不行",
                        "pos": "VH"
                    },
                    {
                        "word": "了",
                        "pos": "T"
                    },
                    {
                        "word": ".",
                        "pos": "PERIODCATEGORY"
                    },
                    {
                        "word": "這",
                        "pos": "Nep"
                    },
                    {
                        "word": "是",
                        "pos": "SHI"
                    },
                    {
                        "word": "環評",
                        "pos": "Na"
                    },
                    {
                        "word": "的",
                        "pos": "DE"
                    },
                    {
                        "word": "結論",
                        "pos": "Na"
                    },
                    {
                        "word": ".",
                        "pos": "PERIODCATEGORY"
                    }
                ],
                "entities": [
                    {
                        "word": "59,000",
                        "type": "CARDINAL",
                        "start": 24,
                        "end": 30
                    },
                    {
                        "word": "5.9萬",
                        "type": "CARDINAL",
                        "start": 34,
                        "end": 38
                    }
                ]
            }
        ]
    }
    ```
    </details>

## Alternative

If you want to run this service without Docker, you can follow this steps after `data` folder is ready.  
However, **we highly recommend using Docker Compose**.

1. Install required packages
    ```bash
    pip3 install -r requirements.txt
    ```
2. Run
    ```bash
    uvicorn app.main:app --host=0.0.0.0 --port=5005
    ```

#!/usr/bin/env python3
from typing import Any

import uvicorn
from ckiptagger import WS, POS, NER
from fastapi import FastAPI
from fastapi.params import Form
from fastapi.requests import Request
from fastapi.responses import RedirectResponse, JSONResponse

app = FastAPI(
    title='CKIP Service',
    description='Web service for ckiplab/ckiptagger'
)
# model variables
app.ws = None
app.pos = None
app.ner = None


@app.on_event('startup')
async def initial() -> None:
    # Load model
    app.ws = WS('./data')
    app.pos = POS('./data')
    app.ner = NER('./data')


@app.get('/', include_in_schema=False)
async def index() -> RedirectResponse:
    return RedirectResponse('/docs')


@app.post('/', response_class=JSONResponse)
async def tokenize(
    request: Request,
    sentence_list: str = Form(
        ...,
        description=r'Sentence list for CKIP tagging, split multiple sentences by linebreak(`\n`)',
        example='美國參議院針對今天總統布希所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。'
    )
) -> dict[str, Any]:
    sentence_list = sentence_list.split('\n')

    word_sentence_list = request.app.ws(sentence_list)
    pos_sentence_list = request.app.pos(word_sentence_list)
    entity_sentence_list = request.app.ner(word_sentence_list, pos_sentence_list)

    json_response = {
        'sentences': [],
    }

    for i in range(len(sentence_list)):
        sentence_result = {
            'segments': [],
            'entities': [],
        }

        sentence_result['segments'] = __get_word_segment_list(
            word_sentence_list[i],
            pos_sentence_list[i],
        )

        for entity in sorted(entity_sentence_list[i]):
            sentence_result['entities'].append({
                'word': entity[3],
                'type': entity[2],
                'start': entity[0],
                'end': entity[1],
            })

        json_response['sentences'].append(sentence_result)

    return json_response


def __get_word_segment_list(word_sentence: list[str], pos_sentence: list[str]) -> list[dict[str, str]]:
    assert len(word_sentence) == len(pos_sentence)
    word_segment_list = []

    for word, pos in zip(word_sentence, pos_sentence):
        word_segment = {
            'word': word,
            'pos': pos,
        }
        word_segment_list.append(word_segment)

    return word_segment_list


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5005)

from typing import Any

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

    words_list = request.app.ws(sentence_list)
    part_of_speech_tags_list = request.app.pos(words_list)
    named_entities_list = request.app.ner(words_list, part_of_speech_tags_list)

    assert len(sentence_list) == len(words_list) == len(part_of_speech_tags_list) == len(named_entities_list)

    json_response = {
        'sentences': [],
    }

    for sentence, words, part_of_speech_tags, named_entities in zip(sentence_list, words_list, part_of_speech_tags_list, named_entities_list):
        sentence_response = {
            'segments': [],
            'entities': []
        }

        for word, part_of_speech_tag in zip(words, part_of_speech_tags):
            sentence_response['segments'].append({
                'word': word,
                'pos': part_of_speech_tag,
            })

        for named_entity in sorted(named_entities):
            sentence_response['entities'].append({
                'word': named_entity[3],
                'type': named_entity[2],
                'start': named_entity[0],
                'end': named_entity[1],
            })

        json_response['sentences'].append(sentence_response)

    return json_response

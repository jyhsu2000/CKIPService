#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
import uvicorn
import json
from ckiptagger import WS, POS, NER
from fastapi import FastAPI
from fastapi.params import Form
from fastapi.responses import PlainTextResponse, RedirectResponse

# model variables
ws = None
pos = None
ner = None

app = FastAPI(
    title="CKIP Service",
    description="Web service for ckiplab/ckiptagger"
)


@app.on_event("startup")
async def initial():
    global ws, pos, ner
    # Load model
    ws = WS("./data")
    pos = POS("./data")
    ner = NER("./data")


@app.get('/', include_in_schema=False)
async def index():
    return RedirectResponse('/docs')


@app.post('/', response_class=PlainTextResponse)
async def tokenize(
        sentence_list: str = Form(
            ...,
            description=r'Sentence list for CKIP tagging, split multiple sentences by linebreak(`\n`)',
            example='美國參議院針對今天總統布希所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。'
        )
):
    global ws, pos, ner
    sentence_list = sentence_list.split('\n')

    word_sentence_list = ws(sentence_list)
    pos_sentence_list = pos(word_sentence_list)
    entity_sentence_list = ner(word_sentence_list, pos_sentence_list)

    # Show results
    json_response = {
        'sentences': [],
    }
    result = []

    def print_word_pos_sentence(word_sentence, pos_sentence):
        assert len(word_sentence) == len(pos_sentence)
        word_pos_sentence = ""
        word_segment_list = []

        for word, pos in zip(word_sentence, pos_sentence):
            word_segment = {
                'word': word,
                'pos': pos,
            }
            word_segment_list.append(word_segment)

        return word_segment_list

    for i in range(len(sentence_list)):
        sentence_result = {
            'segments': [],
            'entities': [],
        }

        sentence_result['segments'] = print_word_pos_sentence(
            word_sentence_list[i],
            pos_sentence_list[i],
        )

        for entity in sorted(entity_sentence_list[i]):
            sentence_result['entities'].append(str(entity))
            result.append(str(entity))
        json_response['sentences'].append(sentence_result)
    return json.dumps(json_response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5005)

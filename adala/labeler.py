import pandas as pd
import json
import os
import logging
import difflib

from typing import List
from langchain import PromptTemplate, OpenAI, LLMChain

logger = logging.getLogger(__name__)


class Labeler:

    PROMPT_TEMPLATE = open(os.path.join(os.path.dirname(__file__), 'prompts', 'labeler.txt')).read()

    def __init__(self):
        self.llm = OpenAI(model_name='text-davinci-003', temperature=0)
        self.llm_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(self.PROMPT_TEMPLATE)
        )

    def match_labels(self, response: str, original_labels: List[str]):
        scores = list(map(lambda l: difflib.SequenceMatcher(None, response, l).ratio(), original_labels))
        return original_labels[scores.index(max(scores))]

    def __call__(self, row: pd.Series, instructions: str, labels: List):
        prediction = self.llm_chain.predict(
            record=json.dumps(row.to_json()),
            instructions=instructions,
            labels=str(labels)
        )
        safe_prediction = self.match_labels(prediction, labels)
        return safe_prediction

from dataclasses import InitVar, dataclass
from typing import Dict, List, Optional, Union

from apiclient import APIClient, Get, endpoint
from httpx import AsyncClient, Client

"""
A wrapper around quizapi (https://quizapi.io)
written in python to support both blocking and async needs
"""

__author__ = "FalseDev"
__title__ = "quizapi"
__copyright__ = "Copyright FalseDev 2021"
__version__ = "0.1.0"
__license__ = "MIT"


@dataclass
class Tag:
    """
    Represents a Tag object
    Questions contain these to inform what they're related to

    Attributes:
        name: Tag name
    """
    name: str

@dataclass
class Question:
    """
    This dataclass represents a Question in the Quiz

    Attributes:
        id: id of the specific question
        question: the question itself
        description: the full description of the question
        correct_answer: **WIP**
        explanation: **WIP**
        tip: **WIP**
        category: the category from which the question is from
        difficulty: difficulty of the question, either `Easy`, `Medium` or `Hard`
        answers: A list of answer options
        tags: A list of `Tag` objects
        correct_answers: A list of correct answers
        multiple_correct_answers: Whether there are multiple correct answers
    """
    id: int
    question: str
    description: Optional[str]
    correct_answer: Optional[str]   # unsure type
    explanation: Optional[None]
    tip: Optional[None]
    category: str
    difficulty: str
    # InitVars
    answers: InitVar[List[str]]
    tags: InitVar[List[Tag]]
    correct_answers: InitVar[List[bool]]
    multiple_correct_answers: InitVar[bool]

    def __post_init__(self, 
            answers:Dict[str, str], 
            tags:List[Dict[str,str]], 
            correct_answers: Dict[str, str],
            multiple_correct_answers:str,
        ):
        self.tags = [Tag(**tag) for tag in tags]
        self.answers = []
        self.correct_answers = []
        for c in range(97,103):
            field1 = 'answer_' + chr(c)
            answer = answers[field1]

            if answer is None:
                break

            field2 = 'answer_' + chr(c) + '_correct'
            self.answers.append(answer)
            self.correct_answers.append(self._to_bool(correct_answers[field2]))

        self.multiple_correct_answers = self._to_bool(multiple_correct_answers)

    @staticmethod
    def _to_bool(inp:str):
        return inp == 'true'


class QuizAPI(APIClient):
    """Class used to create a session with the QuizAPI"""
    base_url = "https://quizapi.io/api/v1"

    def _pre_init(self):
        self._post_processors.append(lambda res: res.json())

    @endpoint
    def get_quiz(self, *, 
            category: Optional[str]=None, 
            limit: Optional[int] = None,
            difficulty: Optional[str] = None,
            tags: Union[List[str], str] = None
        ) -> List[Question]:
        """
        Parameters:
            category: The category of quiz questions to query
            limit: Number of questions to query
        """
        tags_final = None
        if isinstance(tags, list):
            tags_final = ",".join(tags)
        elif isinstance(tags, str):
            tags_final = tags

        params = {"category": category,
                  "limit": limit, "difficulty": difficulty, "tags": tags_final}
        params = {k: params[k]
                  for k in list(filter(lambda arg: params[arg], params))}
        return Get("/questions", params=params)
    
    def _post_get_quiz(self, data):
        if isinstance(data, list):
            return [Question(**q) for q in data] 
        raise RuntimeError()


def create_quiz_api(token: str, *, async_mode:bool=False):
    """
    Creates and returns a `QuizAPI` object with an empty session

    Example:
    ```py
    quiz_api = create_quiz_api("token")
    quiz = quiz_api.get_quiz(category="linux")
    print(quiz)
    ```

    Async Example:
    ```py
    quiz_api = create_quiz_api("token", async_mode=False)
    quiz = await quiz_api.get_quiz(category="linux")
    print(quiz)
    ```
    """
    headers = {'X-Api-Key': token}
    session = AsyncClient(headers=headers) if async_mode else Client(headers=headers)
    return QuizAPI(session=session)


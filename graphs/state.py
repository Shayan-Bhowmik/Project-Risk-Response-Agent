#1. importing typedict and list from typing module 
from typing import TypedDict
from typing import List

#2. defining the riskstate class which will inherit from typedict
class RiskState(TypedDict):

#3. adding all the required fields and their datatypes
    user_input: str
    is_valid_risk: bool
    is_detailed: bool
    followup_questions: List[str]
    strategy: str
    ai_response: str
    rating: str
    current_step: str
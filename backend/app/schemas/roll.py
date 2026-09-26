from pydantic import BaseModel


class RollPatternUpdate(BaseModel):
    pattern_cm: float

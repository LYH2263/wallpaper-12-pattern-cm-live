from pydantic import BaseModel, field_validator

from app.engines.pattern import validate_pattern_cm


class RollPatternUpdate(BaseModel):
    pattern_cm: float

    @field_validator("pattern_cm")
    @classmethod
    def _pattern_non_negative(cls, v):
        return validate_pattern_cm(v)

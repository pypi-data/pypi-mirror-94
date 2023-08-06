"""
Data structures for intent recognition.
"""
import dataclasses
import typing
from dataclasses import dataclass, field
from enum import Enum

from . import utils


@dataclass
class Entity:
    """Named entity from intent."""

    entity: str
    value: str
    raw_value: str = ""
    start: int = 0
    raw_start: int = 0
    end: int = 0
    raw_end: int = 0
    tokens: typing.List[typing.Any] = field(default_factory=list)
    raw_tokens: typing.List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, entity_dict: typing.Dict[str, typing.Any]) -> "Entity":
        """Create Entity from dictionary."""
        return Entity(**utils.only_fields(cls, entity_dict))


@dataclass
class Intent:
    """Named intention with entities and slots."""

    name: str
    confidence: float = 0

    @classmethod
    def from_dict(cls, intent_dict: typing.Dict[str, typing.Any]) -> "Intent":
        """Create Intent from dictionary."""
        return Intent(**utils.only_fields(cls, intent_dict))


@dataclass
class TagInfo:
    """Information used to process FST tags."""

    tag: str
    start_index: int = 0
    raw_start_index: int = 0
    symbols: typing.List[str] = field(default_factory=list)
    raw_symbols: typing.List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, tag_dict: typing.Dict[str, typing.Any]) -> "TagInfo":
        """Create TagInfo from dictionary."""
        return TagInfo(**utils.only_fields(cls, tag_dict))


class RecognitionResult(str, Enum):
    """Result of a recognition."""

    SUCCESS = "success"
    FAILURE = "failure"


@dataclass
class Recognition:
    """Output of intent recognition."""

    result: RecognitionResult
    intent: typing.Optional[Intent] = None
    entities: typing.List[Entity] = field(default_factory=list)
    text: str = ""
    raw_text: str = ""
    recognize_seconds: float = 0
    tokens: typing.List[typing.Any] = field(default_factory=list)
    raw_tokens: typing.List[str] = field(default_factory=list)

    # Transcription details
    wav_seconds: float = 0.0
    transcribe_seconds: float = 0.0
    speech_confidence: float = 0.0

    def asdict(self) -> typing.Dict[str, typing.Any]:
        """Convert to dictionary."""
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, recognition_dict: typing.Dict[str, typing.Any]) -> "Recognition":
        """Create Recognition from dictionary."""

        intent_dict = recognition_dict.pop("intent", None)
        entity_dicts = recognition_dict.pop("entities", None)
        slots_dict = recognition_dict.pop("slots", None)

        intent: typing.Optional[Intent] = None
        if intent_dict:
            intent = Intent.from_dict(intent_dict)
            result = (
                RecognitionResult.SUCCESS if intent.name else RecognitionResult.FAILURE
            )
        else:
            result = RecognitionResult.FAILURE

        recognition = Recognition(
            result=result, intent=intent, **utils.only_fields(cls, recognition_dict)
        )

        if entity_dicts:
            recognition.entities = [Entity.from_dict(e) for e in entity_dicts]

        if slots_dict:
            recognition.entities = [
                Entity(entity=key, value=value) for key, value in slots_dict.items()
            ]

        return recognition

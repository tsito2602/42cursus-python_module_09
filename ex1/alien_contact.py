from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime
from typing import Self


class ContactType(Enum):
    RADIO = 1
    VISUAL = 2
    PHYSICAL = 3
    TELEPATHIC = 4


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_alien_contact(self) -> Self:
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')

        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals should include received messages")

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    print("Valid contact report:")

    valid = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2026, 6, 15, 22, 0, 0),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )

    print(f"ID: {valid.contact_id}")
    print(f"Type: {valid.contact_type}")
    print(f"Location: {valid.location}")
    print(f"Signal: {valid.signal_strength}/10")
    print(f"Duration: {valid.duration_minutes} minutes")
    print(f"Wittness: {valid.witness_count}")

    if valid.message_received:
        print(f"Message: '{valid.message_received}'")

    print()
    print("======================================")

    try:
        _ = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime(2026, 6, 15, 22, 0, 0),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
        )
    except ValidationError as e:
        print("Expected validation error:")
        for error in e.errors():
            message = error.get("ctx", {}).get("error", error["msg"])
            print(message)


if __name__ == "__main__":
    main()

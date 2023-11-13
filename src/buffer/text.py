from dataclasses import dataclass

@dataclass
class Text:
    text: str
    rot_type: str
    status: str

    def __str__(self) -> str:
        return f"text: {self.text[:15]} type: {self.rot_type} status: {self.status}"

    def __repr__(self) -> str:
        return self.__str__()

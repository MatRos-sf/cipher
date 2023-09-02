from dataclasses import dataclass

@dataclass
class Buffer:
    text: str
    rot_type: str
    status: str

    def __str__(self):
        return f"text: {self.text[:15]} type: {self.rot_type} status: {self.status}"

    def __repr__(self):
        return self.__str__()
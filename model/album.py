from dataclasses import dataclass

@dataclass()
class Album:
    id: int
    title: str
    durata: int

    def __str__(self):
        return self.id

    def __repr__(self):
        return self.id

    def __hash__(self):
        return hash(self.id)
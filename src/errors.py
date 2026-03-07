from .utils import TypeAnnotation


class MalformedTypeError(TypeError):
    def __init__(self, typ: TypeAnnotation) -> None:
        super().__init__(f"{typ} is not a valid type.")

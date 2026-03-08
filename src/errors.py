from .utils import TypeAnnotation


class MalformedTypeError(TypeError):
    def __init__(self, typ: TypeAnnotation, *, extra_msg: str = "") -> None:
        msg = f"{typ} is not a valid type."
        if extra_msg:
            assert extra_msg == extra_msg.strip()
            assert extra_msg[-1] in ".!?"
            msg += f" {extra_msg}"
        super().__init__(msg)

    @classmethod
    def requires_arguments_message(cls, typ: TypeAnnotation) -> str:
        return f"{typ} requires type arguments."

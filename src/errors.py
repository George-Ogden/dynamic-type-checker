from .utils import TypeAnnotation


class MalformedTypeError(TypeError):
    def __init__(self, typ: TypeAnnotation, *, extra_msg: str = "") -> None:
        self.typ = typ
        super().__init__(self.make_msg(extra_msg))

    def make_msg(self, extra_msg: str) -> str:
        msg = f"{self.typ} is not a valid type."
        if extra_msg:
            assert extra_msg == extra_msg.strip()
            assert extra_msg[-1] in ".!?"
            msg += f" {extra_msg}"
        return msg

    @classmethod
    def requires_arguments_message(cls, typ: TypeAnnotation) -> str:
        return f"{typ} requires type arguments."

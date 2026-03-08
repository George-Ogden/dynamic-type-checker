from .utils import TypeAnnotation


class MalformedTypeError(TypeError):
    def __init__(
        self, typ: TypeAnnotation, *, requires_arguments: bool = False, extra_msg: str = ""
    ) -> None:
        msg = f"{typ} is not a valid type."
        if requires_arguments:
            msg += f" {typ} requires type arguments."
        if extra_msg:
            assert extra_msg == extra_msg.strip()
            assert extra_msg[-1] in ".!?"
            msg += f" {extra_msg}"
        super().__init__(msg)

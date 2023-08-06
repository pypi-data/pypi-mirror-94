import dataclasses


@dataclasses.dataclass(frozen=True)
class ScanResult:
    successful: bool
    message: str

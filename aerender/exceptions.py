class AERenderError(Exception):
    pass


class CompositionNotFoundError(AERenderError):
    pass


class AfterEffectsError(AERenderError):
    pass


class PathNotFoundError(AfterEffectsError):
    pass

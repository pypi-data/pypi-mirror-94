from . import error, resolver

NotFoundError = error.NotFoundError
NotStringValueError = error.NotStringValueError
CircularReferenceError = error.CircularReferenceError

resolve = resolver.Resolver().resolve

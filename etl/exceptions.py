class ETLError(Exception):
    """Base class for ETL errors"""
    pass


class ExtractionError(ETLError):
    """Raised when extraction fails"""
    pass


class TransformationError(ETLError):
    """Raised when transformation fails"""
    pass


class LoadError(ETLError):
    """Raised when loading to DB fails"""
    pass

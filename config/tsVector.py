from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import TSVECTOR

class TSVector(TypeDecorator):
    impl = TSVECTOR
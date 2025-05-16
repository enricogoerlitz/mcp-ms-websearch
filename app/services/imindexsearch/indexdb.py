import evars
import gvars


from services.imindexsearch.base import IInMemoryIndexDB
from services.imindexsearch.hnsw import HNSWInMemoryIndexDB


class InMemoryIndexDBFactory:
    @staticmethod
    def create(type: str) -> IInMemoryIndexDB:
        match type:
            case gvars.INDEXDB_TYPE_HNSW:
                return HNSWInMemoryIndexDB()
            case _:
                raise ValueError(f"Unsupported indexdb type: {type}")

    @staticmethod
    def new() -> IInMemoryIndexDB:
        index: IInMemoryIndexDB = InMemoryIndexDBFactory.create(evars.INDEXDB_TYPE)
        return index

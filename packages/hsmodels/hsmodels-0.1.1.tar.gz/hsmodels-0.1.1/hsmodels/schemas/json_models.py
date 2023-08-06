from typing import Dict, List

from pydantic import AnyUrl, BaseModel, validator

from hsmodels.schemas.enums import UserIdentifierType


class User(BaseModel):
    name: str = None
    email: str = None
    url: AnyUrl = None
    phone: str = None
    address: str = None
    organization: str = None
    website: str = None
    identifiers: Dict[UserIdentifierType, str] = {}


class ResourcePreview(BaseModel):
    resource_type: str = None
    resource_title: str = None
    resource_id: str = None
    abstract: str = None
    authors: List[str] = []
    creator: str = None
    doi: str = None
    date_created: str = None
    date_last_updated: str = None
    public: bool = None
    discoverable: bool = None
    shareable: bool = None
    coverages: Dict[str, str] = {}
    immutable: bool = None
    published: bool = None
    resource_url: str = None
    resource_map_url: str = None
    resource_metadata_url: str = None

    @validator("authors", pre=True)
    def handle_null_author(cls, v):
        if v is None:
            return []

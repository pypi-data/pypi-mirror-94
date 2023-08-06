from pydantic import BaseModel, UUID4


class AuthFirstPhaseRequest(BaseModel):
    name: str

    class Config:
        allow_mutation = False


class AuthFirstPhaseResponse(BaseModel):
    offline: bool
    serverId: str
    verifyToken: int

    class Config:
        allow_mutation = False


class AuthSecondPhaseRequest(AuthFirstPhaseRequest):
    verifyToken: int

    class Config:
        allow_mutation = False


class AuthSecondPhaseResponse(BaseModel):
    accessToken: UUID4
    userId: UUID4

    class Config:
        allow_mutation = False


class AuthCookie(BaseModel):
    ip: str
    token: int

    class Config:
        allow_mutation = False

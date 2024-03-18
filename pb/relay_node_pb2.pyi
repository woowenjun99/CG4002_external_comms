from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Values(_message.Message):
    __slots__ = ("acceleration_x", "acceleration_y", "acceleration_z", "gyro_x", "gyro_y", "gyro_z")
    ACCELERATION_X_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_Y_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_Z_FIELD_NUMBER: _ClassVar[int]
    GYRO_X_FIELD_NUMBER: _ClassVar[int]
    GYRO_Y_FIELD_NUMBER: _ClassVar[int]
    GYRO_Z_FIELD_NUMBER: _ClassVar[int]
    acceleration_x: float
    acceleration_y: float
    acceleration_z: float
    gyro_x: float
    gyro_y: float
    gyro_z: float
    def __init__(self, acceleration_x: _Optional[float] = ..., acceleration_y: _Optional[float] = ..., acceleration_z: _Optional[float] = ..., gyro_x: _Optional[float] = ..., gyro_y: _Optional[float] = ..., gyro_z: _Optional[float] = ...) -> None: ...

class FromRelayNodeRequest(_message.Message):
    __slots__ = ("values", "player_id", "shoot_detected", "ir_detected", "test_action")
    VALUES_FIELD_NUMBER: _ClassVar[int]
    PLAYER_ID_FIELD_NUMBER: _ClassVar[int]
    SHOOT_DETECTED_FIELD_NUMBER: _ClassVar[int]
    IR_DETECTED_FIELD_NUMBER: _ClassVar[int]
    TEST_ACTION_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[Values]
    player_id: int
    shoot_detected: bool
    ir_detected: bool
    test_action: str
    def __init__(self, values: _Optional[_Iterable[_Union[Values, _Mapping]]] = ..., player_id: _Optional[int] = ..., shoot_detected: bool = ..., ir_detected: bool = ..., test_action: _Optional[str] = ...) -> None: ...

class Player(_message.Message):
    __slots__ = ("hp", "bullets", "bombs", "shield_hp", "deaths", "shields")
    HP_FIELD_NUMBER: _ClassVar[int]
    BULLETS_FIELD_NUMBER: _ClassVar[int]
    BOMBS_FIELD_NUMBER: _ClassVar[int]
    SHIELD_HP_FIELD_NUMBER: _ClassVar[int]
    DEATHS_FIELD_NUMBER: _ClassVar[int]
    SHIELDS_FIELD_NUMBER: _ClassVar[int]
    hp: int
    bullets: int
    bombs: int
    shield_hp: int
    deaths: int
    shields: int
    def __init__(self, hp: _Optional[int] = ..., bullets: _Optional[int] = ..., bombs: _Optional[int] = ..., shield_hp: _Optional[int] = ..., deaths: _Optional[int] = ..., shields: _Optional[int] = ...) -> None: ...

class FromRelayNodeResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GameStateRequest(_message.Message):
    __slots__ = ("player_one", "player_two")
    PLAYER_ONE_FIELD_NUMBER: _ClassVar[int]
    PLAYER_TWO_FIELD_NUMBER: _ClassVar[int]
    player_one: Player
    player_two: Player
    def __init__(self, player_one: _Optional[_Union[Player, _Mapping]] = ..., player_two: _Optional[_Union[Player, _Mapping]] = ...) -> None: ...

class GameStateResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

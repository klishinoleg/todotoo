from enum import Enum


class LogMessageType(str, Enum):
    ALREADY_EXIST = "already_exist"
    NOT_FOUND = "not_found"
    OBJ_CREATED = "obj_created"
    OBJ_DELETED = "obj_deleted"
    OBJ_UPDATED = "obj_updated"
    MEASURE_FUNC_TIME = "measure_func_time"
    IDEA_CREATE_FAILED = "idea_create_failed"

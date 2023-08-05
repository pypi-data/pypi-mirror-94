"""
Module providing types describing API responses
"""

from typing import \
    Dict, List, Literal, Optional, \
    TypedDict, NewType

UserID = NewType("UserID", int)
ModuleID = NewType("ModuleID", int)
ActivityID = NewType("ActivityID", int)
GroupID = NewType("GroupID", int)


class Student(TypedDict):
    id: UserID
    login: str
    firstname: str
    lastname: str


class RegisteredGroupMember(Student):
    validation: Literal[0, 1]
    forced: Literal[0, 1]


class Group(TypedDict):
    id: GroupID
    leader: Student
    members: List[RegisteredGroupMember]
    rendu: str


class Identity(TypedDict):
    id: UserID
    login: str
    email: str
    logas: bool
    groups: List[str]
    login_date: str
    firstconnexion: bool


class _ActivityModuleInfo(TypedDict):
    id: ModuleID
    name: str
    published: int
    mandatory: Literal["mandatory", "notMandatory"]
    start: str
    end: str


class ActivityBasicInfo(TypedDict):
    name: str
    type: str
    duration: int
    min_student: int
    max_student: int
    coefficient: float
    eliminate: Optional[float]
    date_start: str
    date_end: str
    registration_date: str


class ActivityCreationInfo(ActivityBasicInfo):
    pass


class ActivityInfo(ActivityBasicInfo):
    id: ActivityID
    rendu: str
    has_moulinette: Optional[bool]
    total_stages: Optional[int]
    module: _ActivityModuleInfo


class ModuleBasicInfo(TypedDict):
    version: int
    name: str
    long_name: str
    duration: int
    published: int
    mandatory: Literal["mandatory", "notMandatory"]
    description: str
    equivalence: Optional[str]


class ModuleCreationInfo(ModuleBasicInfo):
    average: int
    nb_marks: Optional[int]


class ModuleInfo(ModuleCreationInfo):
    uv_id: int
    uv_name: str
    id: ModuleID
    start: str
    end: str
    activities: Optional[List]


class StudentModule(ModuleBasicInfo):
    date_end: str
    date_start: str
    id: ModuleID
    uv_id: int
    uv_name: str
    validation: Optional[Literal["Validée", "Non validée"]]


class Teacher(TypedDict):
    id: UserID
    login: str
    user_id: UserID
    email: str
    status: Literal["prof", "chef", "asset"]


class ChecklistStep(TypedDict):
    name: str
    coeff: float
    marks: List[float]
    default: float
    commentaire: str


class ChecklistComment(TypedDict):
    prof: str
    commentaire: str
    students: List[UserID]


class Checklist(TypedDict):
    intro: str
    etapes: List[ChecklistStep]
    commentaires: List[ChecklistComment]


class IndividualMark(TypedDict):
    login: str
    cheater: bool
    absent: bool
    no_delivery: bool
    checklist_mark: float
    personnals: List


class Marks(TypedDict):
    checklist: Checklist
    students: Dict[str, IndividualMark]

from .roles import UserRoles


class PublicAccess:
    pass


class Group:
    members: frozenset[UserRoles]

    def __init__(self, *members: UserRoles):
        self.members = frozenset(members)


PermissionAcl = UserRoles | Group | PublicAccess


class Permissions:
    __ORGANIZERS = Group(UserRoles.Admin, UserRoles.Organizer)
    __PRIVILEGED = Group(UserRoles.Judge, UserRoles.Organizer, UserRoles.Admin)

    ReadHackathonList = PublicAccess()
    ReadHackathonInfo = PublicAccess()
    ReadHackathonTeams = PublicAccess()

    CreateHackathon = __ORGANIZERS
    DeleteHackathon = __ORGANIZERS
    UpdateHackathon = __ORGANIZERS
    ScoreHackathon = __ORGANIZERS

    ReadAdminHackathonTeamMates = __PRIVILEGED
    ReadAdminHackathonCriteria = __PRIVILEGED

    CreateCriterion = __ORGANIZERS
    UpdateCriterion = __ORGANIZERS
    DeleteCriterion = __ORGANIZERS

    GetJudges = __PRIVILEGED
    CreateJudge = __ORGANIZERS
    DeleteJudge = __ORGANIZERS

    ReadTeamScores = __PRIVILEGED
    CreateTeamScore = UserRoles.Judge


def perform_check(acl: PermissionAcl, role: UserRoles) -> bool:
    if isinstance(acl, PublicAccess):
        return True
    elif isinstance(acl, UserRoles):
        return role is acl

    return role in acl.members

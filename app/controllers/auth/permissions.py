from app.controllers.auth.roles import UserRoles


class PublicAccess:
    pass


class Group:
    members: frozenset[UserRoles]

    def __init__(self, *members: UserRoles):
        self.members = frozenset(members)


PermissionAcl = UserRoles | Group | PublicAccess


class Permissions:
    ReadHackathonList = PublicAccess()
    ReadHackathonInfo = PublicAccess()
    ReadHackathonTeams = PublicAccess()

    CreateHackathon = UserRoles.Admin
    DeleteHackathon = UserRoles.Admin
    UpdateHackathon = UserRoles.Admin

    ReadAdminHackathonTeamMates = Group(
        UserRoles.Judge, UserRoles.Organizer, UserRoles.Admin
    )
    ReadAdminHackathonCriteria = Group(
        UserRoles.Judge, UserRoles.Organizer, UserRoles.Admin
    )

    CreateCriterion = Group(UserRoles.Judge, UserRoles.Admin)
    UpdateCriterion = Group(UserRoles.Judge, UserRoles.Admin)
    DeleteCriterion = Group(UserRoles.Judge, UserRoles.Admin)

    ReadTeamScores = Group(
        UserRoles.Judge, UserRoles.Organizer, UserRoles.Admin
    )
    CreateTeamScore = UserRoles.Judge


def perform_check(acl: PermissionAcl, role: UserRoles) -> bool:
    if isinstance(acl, PublicAccess):
        return True
    elif isinstance(acl, UserRoles):
        return role is acl

    return role in acl.members

import logging

from django.utils.translation import gettext as _

from participants.models import Team
from utils.views import BadJsonRequestError

from ..conflicts import ConflictsInfo, HistoryInfo

logger = logging.getLogger(__name__)

registry = {}


def register(cls):
    registry[cls.key] = cls
    return cls


class BaseAdjudicatorAllocator:

    def __init__(self, debates, adjudicators, round):
        self.tournament = round.tournament
        self.round = round
        self.debates = list(debates)
        self.adjudicators = adjudicators

        if len(self.adjudicators) == 0:
            info = _("There are no available adjudicators. Ensure there are "
                     "adjudicators who have been marked as available for this "
                     "round before auto-allocating.")
            logger.info(info)
            raise BadJsonRequestError(info)

        teams = Team.objects.filter(debateteam__debate__in=debates)
        self.conflicts = ConflictsInfo(teams=teams, adjudicators=self.adjudicators)
        self.history = HistoryInfo(round=round)

    def allocate(self):
        raise NotImplementedError

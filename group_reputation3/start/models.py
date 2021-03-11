from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

class Constants(BaseConstants):
    name_in_url = 'start'
    players_per_group = None
    num_rounds = 1
    

class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    accept = models.BooleanField(
        doc="""Whether subject accepts the consent form""",
        widget=widgets.RadioSelect,
        choices=[[True, 'Accept'], [False, 'Reject']]
    )
from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class AllWait(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number == 1


class Instructions(Page):

    def is_displayed(self):
        return self.round_number == 1


class Comprehension(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def get_form_fields(self):
        if self.round_number == 1:
            return ['comp1']

    def error_message(self, values):
        if values['comp1'] != "-2 points":
            self.player.comp1_wrong += 1
            return "Incorrect answer"


class Comprehension2(Page):
    form_model = 'player'

    def is_displayed(self):
        return self.round_number == 1

    def get_form_fields(self):
        if self.round_number == 1:
            return ['comp2']

    def error_message(self, values):
        if values['comp2'] != "Play DEFER":
            self.player.comp2_wrong += 1
            return "Incorrect answer"


class Role1(Page):
    form_model = 'group'
    form_fields = ['r1_action']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def vars_for_template(self):
        return {
            'round_number': self.round_number
        }

    def before_next_page(self):
        if self.round_number == 1:
            for p in self.group.get_players():
                p.participant.payoff = c(Constants.initial_payoff)


class ProcessingPage(WaitPage):
    pass


class Role2(Page):
    form_model = 'group'

    def is_displayed(self):
        return self.player.id_in_group == 2

    def get_form_fields(self):
        if self.group.r1_action == "CHALLENGE":
            return ['r2_action']
        else:
            return []

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'r1_action': self.group.r1_action
        }


class ProcessingPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Outcome(Page):

    def vars_for_template(self):
        return {
            'round_number': self.round_number,
            'r1_action': self.group.r1_action,
            'r2_action': self.group.r2_action,
            'payoff': self.player.payoff,
            'final_payoff': self.participant.payoff
        }


class End(Page):

    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'total_earnings': self.participant.payoff
        }

    def before_next_page(self):
        if 'summary_data' in self.participant.vars:
            self.participant.vars['summary_data'].append(('Task 1', self.participant.payoff))


page_sequence = [
    AllWait,
    Instructions,

    Comprehension,
    Comprehension2,

    Role1,
    ProcessingPage,
    Role2,
    ProcessingPage2,
    Outcome,

    End
]
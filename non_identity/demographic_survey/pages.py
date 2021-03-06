from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Main(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']

    def vars_for_template(self):
        return {
            'treatment': self.session.config['treatment']
        }


page_sequence = [Main]

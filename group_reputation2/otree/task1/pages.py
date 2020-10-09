from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import shared
import random, math


class Main(Page):
    form_model = 'player'
    form_fields = ['birth_region', 'other_br', 'pi_q1', 'pi_q2', 'pi_q3', 'pi_q4', 'pi_q5', 'pi_q6', 'pi_q7']

    def error_message(self, values):
        if values['birth_region'] == Constants.br_info['other_val'] and values['other_br'] is None:
            return 'Other birth region was selected but not specified'


class FormGroups(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        br_info = Constants.br_info
        pi_info = Constants.pi_info
        num_per_group = Constants.players_per_group

        # find the political ideology of players
        for p in self.subsession.get_players():
            p.set_pi_score()
        scores = [p.pi_score for p in self.subsession.get_players()]
        scores.sort()
        # subjects are categorised by political ideology. those with highest scores
        # are coded 1 and those with lowest scores 3, with neutrals as 2.
        # thresholds are defined in /shared.py lines 2 and 3. ideology groups
        # will not be formed based on shared neutral ideology. For example
        # if there are two 2's and one 1 then they will be in the no group
        # condition
        low_per = scores[math.ceil(shared.low_perc * len(scores)) - 1]
        high_per = scores[math.ceil(shared.high_perc * len(scores)) - 1]
        for p in self.subsession.get_players():
            if p.pi_score >= high_per:
                p.pol_ideology = 1
            elif p.pi_score <= low_per:
                p.pol_ideology = 3
            else:
                p.pol_ideology = 2

        # setup array
        players = []  # holds players that are still left to sort
        for p in self.subsession.get_players():
            players.append({
                'id': p.participant.id_in_session,
                'birth_region': p.birth_region,
                'pol_ideology': p.pol_ideology
            })

        # for the regions that have players with less than Constants.min_br set them to the other type
        players = shared.set_reduced_br(players.copy(), 3, br_info['other_val'])
        random.shuffle(players)

        # sort based on birth region
        new_groups, players = shared.create_groups(players.copy(), br_info, num_per_group)
        final_groups = shared.set_roles(new_groups.copy(), 'birth_region', num_per_group)
        random.shuffle(players)

        # sort based on political ideology
        new_groups, players = shared.create_groups(players.copy(), pi_info, num_per_group)
        final_groups = final_groups + shared.set_roles(new_groups.copy(), 'pol_ideology', num_per_group)
        random.shuffle(players)

        # randomly group the rest
        new_groups = shared.create_random_groups(players.copy(), num_per_group)
        final_groups = final_groups + shared.set_roles(new_groups.copy(), None, num_per_group)

        # set participant data so this shared across apps (tasks)
        for i in range(len(final_groups)):
            for p in final_groups[i]:
                for player in self.subsession.get_players():
                    if player.participant.id_in_session == p['id']:
                        player.rl = p['role']
                        player.sorted_by = p['sorted_by']
                        player.participant.vars['group'] = i
                        player.participant.vars['role'] = p['role']
                        player.participant.vars['sorted_by'] = p['sorted_by']
                        player.participant.vars['birth_region'] = p['birth_region']
                        player.participant.vars['pol_ideology'] = p['pol_ideology']

        shared.print_to_console(final_groups)


page_sequence = [
    Main,
    FormGroups
]
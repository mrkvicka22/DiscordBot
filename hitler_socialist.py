import random
choosable_fas_eve = ['none', 'peek', 'investigation', 'shoot',  'special election', 'shot veto']
choosable_soc_eve = ['none', 'bugging', 'recruitment', '5yp',  'confession','censorship',
                     'confession', 'veto']


''' ukazka ako moze vyzerat setup list - l[0] -> pocty hracov v timoch, l[1] -> policy tracks
 length l[2] -> kolko akych zakonov, l[3][0-2] -> events, l[4]->hz default'''
example_setup_list = [[3,1,2],[5,5,6],[5,7,10][['none','none','none','none','victory'],
                                               ['bugging','recruitment','5yp','confession','victory'],
                                               ['investigation','peek','special election','shot','shot veto','victory']]]

class Player():

    def __init__(self, role):
        self.role = role





def setup(number_of_players, setup_lst=None):

    # Setupujem hru podla https://docs.google.com/spreadsheets/d/1kGwuHEP4FIGTJIu3TiQ4IUvd-YsXonK1-wUKuimX6B4/edit#gid=808475860
    if setup_lst is None:

        if number_of_players == 6:
            return [{'lib':3, 'soc':1, 'fas':1, 'hit':1}, [5, 5, 6], [5, 7, 10],[['none', 'none', 'none', 'none', 'victory'],
                                                      ['bugging', 'recruitment', '5yp', 'confession', 'victory'],
                                                      ['investigation','peek','special election','shot','shot veto','victory']],[3]]
        elif number_of_players == 7:
            return [{'lib':4, 'soc':1, 'fas':1, 'hit':1}, [5, 5, 6], [5, 8, 10], [['none', 'none', 'none', 'none', 'victory'],
                                                       ['bugging', 'recruitment', '5yp', 'confession', 'victory'],
                                                       ['investigation','peek','special election','shot','shot veto','victory']],[3]]
        elif number_of_players == 9:
            return [{'lib':4, 'soc':2, 'fas':2, 'hit':1}, [5, 6, 6], [5, 7, 10], [['none', 'none', 'none', 'none', 'victory'],
                                                       ['none', 'recruitment censorship', '5yp', 'congress' 'confession', 'victory'],
                                                       ['none','investigation','special election','shot','shot veto','victory']],[3]]
        elif number_of_players == 13:
            return [{'lib':6, 'soc':3, 'fas':3, 'hit':1}, [5, 6, 6], [5, 7, 10], [['none', 'none', 'peek', 'none', 'victory'],
                                                       ['none', 'recruitment censorship', '5yp','recruitment', 'confession', 'victory'],
                                                       ['investigation','peek','special election','shot','shot veto','victory']],[3]]
        else:
            return 0

    # mozno chcem davat inputy na lahke vytvorenie setupu do elsu...
    else:
        return setup_lst

def asssign_roles(players_lst, setup_lst):
    players_classes = []
    for i in range(len(players_lst)):
        for dickey in setup_lst[0]:
            for role in range(setup_lst[0][dickey]):
                player = Player(role)
                players_classes.append(player)
    random.shuffle(players_classes)
    return zip(players_lst,players_classes)


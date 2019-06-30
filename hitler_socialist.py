from random import shuffle
from itertools import cycle


choosable_fas_eve = ['none', 'peek', 'investigation', 'shoot',  'special election', 'shot veto']
choosable_soc_eve = ['none', 'bugging', 'recruitment', '5yp',  'confession','censorship',
                     'confession', 'veto']


''' ukazka ako moze vyzerat setup list - l[0] -> pocty hracov v timoch, l[1] -> policy tracks
 length l[2] -> kolko akych zakonov, l[3][0-2] -> events, l[4]->hz default'''
example_setup_list = [[3,1,2],[5,5,6],[5,7,10],[['none','none','none','none','victory'],
                                               ['bugging','recruitment','5yp','confession','victory'],
                                               ['investigation','peek','special election','shot','shot veto','victory']]]

players_names = ['ferko', 'jozko', 'dezko', 'matko', 'franto', 'tomco']


def setup(number_of_players, setup_lst=None):

    # Setupujem hru podla https://docs.google.com/spreadsheets/d/1kGwuHEP4FIGTJIu3TiQ4IUvd-YsXonK1-wUKuimX6B4/edit#gid=808475860
    if setup_lst is None:

        if number_of_players == 6:
            return [[3,1,1,1], [5, 5, 6], [5, 7, 10],[['none', 'none', 'none', 'none', 'victory'],
                                                      ['bugging', 'recruitment', '5yp', 'confession', 'victory'],
                                                      ['investigation','peek','special election','shot','shot veto','victory']],[3]]
        elif number_of_players == 7:
            return [[4,1,1,1], [5, 5, 6], [5, 8, 10], [['none', 'none', 'none', 'none', 'victory'],
                                                       ['bugging', 'recruitment', '5yp', 'confession', 'victory'],
                                                       ['investigation','peek','special election','shot','shot veto','victory']],[3]]
        elif number_of_players == 9:
            return [[4,2,2,1], [5, 6, 6], [5, 7, 10], [['none', 'none', 'none', 'none', 'victory'],
                                                       ['none', 'recruitment censorship', '5yp', 'congress' 'confession', 'victory'],
                                                       ['none','investigation','special election','shot','shot veto','victory']],[3]]
        elif number_of_players == 13:
            return [[6,3,3,1], [5, 6, 6], [5, 7, 10], [['none', 'none', 'peek', 'none', 'victory'],
                                                       ['none', 'recruitment censorship', '5yp','recruitment', 'confession', 'victory'],
                                                       ['investigation','peek','special election','shot','shot veto','victory']],[3]]
        else:
            return 0

    # mozno chcem davat inputy na lahke vytvorenie setupu do elsu...
    else:
        return setup_lst


def create_deck(setup: list) -> list:
    cards = setuplst[2]
    deck = []
    for i in cards:
        for j in range(i):
            deck.append(cards.index(i))
    changer_dic = {0: 'lib_card', 1: 'soc_card', 2: 'fas_card'}
    deck = [changer_dic.get(n, n) for n in deck]

    shuffle(deck)
    print('deck\n',deck)
    return deck

discard_pile = []
setuplst = setup(len(players_names))
deck = create_deck(setuplst)


class Player():

    def __init__(self, role, meno):
        self.role = role
        self.hlasy_hraca = []
        self.name = meno

    def vote(self):
        while 1:
            hlas = input('Ja/Nein')
            if hlas.lower() == 'ja' or hlas.lower() == 'nein':
                break
            else:
                print('invalid input vote again')

        self.hlasy_hraca.append(hlas)
        return hlas

    def pres_laws_pass(self):
        cards = draw(3, deck)
        print(cards)
        discard_pick = int(input('choose card to discard 1-3')) - 1
        discard_pile.append(cards[discard_pick])
        cards.pop(discard_pick)
        return cards, discard_pile

    def chanc_laws_pass(self, pres_passed):
        print(pres_passed)
        discard_pick = int(input('choose one card to discard 1-2')) - 1
        discard_pile.append(pres_passed[discard_pick])
        pres_passed.pop(discard_pick)
        return pres_passed, discard_pile

    def pres_kill(self, active_players: list, dead_players: list) -> tuple:
        player_to_exe = int(input(f'choose a player to execute 1-{len(players)}')) - 1
        dead_players.append(active_players[player_to_exe])
        active_players.pop(player_to_exe)
        return active_players, dead_players

    def choose_chancellor(self, last_chancellor, last_president):
        avaiable_players = players.copy()
        avaiable_players.remove(self)
        if last_chancellor != self and last_president != self:
            avaiable_players.remove(last_chancellor)
        if last_president != self and last_chancellor != self:
            avaiable_players.remove(last_president)

        # nejako ukazat prezidentovi kto moze byt kancelar
        for i, plyr in enumerate(avaiable_players):
            print(i, plyr.name, plyr.role)
        print(len(players))
        not_correctinput = 1
        while not_correctinput:
            chanc_indx = int(input('choose your chancellor'))
            if 0 <= chanc_indx < len(avaiable_players):
                not_correctinput = 0

        return avaiable_players[chanc_indx]

def create_player_classes_list():
    # vytvorim kazdemu hracovi classu s rolou, ktoru mu priradim a zaradim ich do timov.

    players_classes = []
    roles = setuplst[0]
    role_list = []
    global fascists
    global liberals
    global socialsts
    global hitler
    socialsts = []
    liberals = []
    fascists = []
    hitler = None

    # zo setupu vytvaram list, z ktoreho potom nahodne priradujem hracov list vyzera takto: ['lib_player', 'lib_player', 'lib_player', 'soc_player', 'fas_player', 'hit_player']
    for f, i in enumerate(roles):
        for j in range(i):
            role_list.append(f)
    changer_dic = {0: 'lib_player', 1: 'soc_player', 2: 'fas_player', 3:'hit_player'}
    role_list = [changer_dic.get(n, n) for n in role_list]

    #nahodne priradujem hracom rolu pricom im vytvaram classu a pridavam ich do timov
    shuffle(role_list)
    for i in range(len(players_names)):
        player = Player(role_list[i],players_names[i])
        players_classes.append(player)
        if player.role == 'fas_player':
            fascists.append(player)
        elif player.role == 'lib_player':
            liberals.append(player)
        elif player.role == 'soc_player':
            socialsts.append(player)
        elif player.role == 'hit_player':
            hitler = player
        else:
            raise(NotImplementedError)

    return players_classes

# vytvaram premmennu players ktora sa sklada z class Player(). Potom to printujem nech to pekne vidim.
players = create_player_classes_list()
for i, plyr in enumerate(players):
    print(i, plyr.name, plyr.role)

# vyberam prveho prezidenta a vytvaram presidentloop. Ten je dolezity aby sa pekne menili prezidenti len pomocou next().
# last_president a last_chancellor maju placeholder hodnotu president
president = players[0]
presidentloop = cycle(players)
last_president = president
last_chancellor = president


# vsetci hraci postupne hlasuju pomocou Player().vote()
def collect_votes():
    all_votes =[]
    for plyr in players:
        all_votes.append(plyr.vote())
    return all_votes


# tato funkcia je zbytocna ale zdala sa mi fajn do buducnosti.
def draw(number_of_cards,deck):
    drawn_cards = []
    for i in range(number_of_cards):
        drawn_cards.append(deck[0])
        deck.pop(0)

    return drawn_cards


def turn(president):
    global last_president
    global last_chancellor

    passed = False
    chancellor = president.choose_chancellor(last_president,last_chancellor)
    print(f'we are voting for president {president.name} and chancellor {chancellor.name}')
    all_votes = collect_votes()
    if all_votes.count('Ja') > len(players)//2:
        passed = True
        last_president = president
        last_chancellor = chancellor
        pres_laws, discard_pile = president.pres_laws_pass()
        enacted_policy, discard_pile = chancellor.chanc_laws_pass(pres_laws)
        print(f'everyone {enacted_policy} was enacted')
    else:
        passed = False

    president = next(presidentloop)
    print(f'next president is {president.name}')
    turn(president)
turn(president)
# def game():
#     #spoznavanie(players)
#     while True:
#         turn(president)

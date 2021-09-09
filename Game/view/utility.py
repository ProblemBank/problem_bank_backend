from random import choice

from django.db.transaction import atomic

from Game.models import Player


def get_random(query_set):
    pks = query_set.values_list('pk', flat=True).order_by('id')
    random_pk = choice(pks)
    return query_set.get(pk=random_pk)


@atomic
def make_notification(player: Player, value: int):
    player.save()

    # new_transaction = Transaction()
    # new_transaction.player = player
    # new_transaction.title = title
    # new_transaction.amount = value
    #
    # new_transaction.save()

from django.contrib.auth.models import User
from adventure.models import Player, Room


Room.objects.all().delete()

r_outside = Room(title="Outside Soldier Field",
               description="North of you, you see the ticketing gate")

r_foyer = Room(title="You arrived at the ticketing Gate", description="""Please pay to proceed! P.S It's pretty expensive!""")

r_overlook = Room(title="You found your seat!", description="""You can barely see the field.""")

r_narrow = Room(title="The game started", description="""Trubisky throws a pick on the first snap! You're pulling your hair out!""")

r_treasure = Room(title="Final drive!", description="""Somehow Trubisky has kept you in the game, you're down one point and are at the 43 yard line! Out comes the kicker all needs to do is make this last field goal and you win the game!""")

r_outside.save()
r_foyer.save()
r_overlook.save()
r_narrow.save()
r_treasure.save()

# Link rooms together
r_outside.connectRooms(r_foyer, "n")
r_foyer.connectRooms(r_outside, "s")

r_foyer.connectRooms(r_overlook, "n")
r_overlook.connectRooms(r_foyer, "s")

r_foyer.connectRooms(r_narrow, "e")
r_narrow.connectRooms(r_foyer, "w")

r_narrow.connectRooms(r_treasure, "n")
r_treasure.connectRooms(r_narrow, "s")

players=Player.objects.all()
for p in players:
  p.currentRoom=r_outside.id
  p.save()


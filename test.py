from main import *
import time

with Rcon("127.0.0.1", "FalswIsNotCute", 25575):

    pr = particler((0,80,0),default_delta=(0.1,1,0.1), default_count=10)
    c = pr.get_canvas()
    c.set_density(1)

    c.get_pen(
    ).line((-20, 0 ,-20), (20, 20, 20), name="flame", duration=1
    ).line((20, 0, -20), (-20, 0, 20), name="flame"
    ).throw()

    c.show()
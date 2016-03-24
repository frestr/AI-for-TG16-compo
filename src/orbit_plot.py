target_movement = target.get_movement(int(5*1000/50))
missile_movement = missile.get_movement(int(5*1000/50))

import matplotlib.pyplot as plt
tx = []; ty = []; mx = []; my=[]
for pos in target_movement:
    tx.append(pos.x)
    ty.append(pos.y)
for pos in missile_movement:
    mx.append(pos.x)
    my.append(pos.y)

# print(tx)
plt.xlim([-1, 1])
plt.ylim([-1, 1])
plt.plot(tx, ty)
plt.show()


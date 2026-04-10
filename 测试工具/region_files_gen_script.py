import os

x_range = [-16,16]
z_range = [-16,16]

os.makedirs('gen_regions',exist_ok=True)

for x in range(x_range[0],x_range[1]): 
    for z in range(z_range[0],z_range[1]): 
        name = f'r.{x}.{z}.mca'
        with open(os.path.join('gen_regions',name),'w') as f: 
            f.write(f'{x},{z}')
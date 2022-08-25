import pulp
import pandas as pd

sites_df = pd.read_csv('sites.csv')
lanes_df = pd.read_csv('transportation_lanes.csv')
# nodes
S = list(sites_df[sites_df['Site Type'] == 'Station']['Origin Site'])
H = list(sites_df[sites_df['Site Type'] == 'Hub']['Origin Site'])
I = S + H
# arcs
arcs = list(zip(lanes_df['Origin Site'], lanes_df['Dest. Site']))
# transit distance
td = dict(zip(zip(lanes_df['Origin Site'], lanes_df['Dest. Site']), lanes_df['Transit Distance (Km)']))
# arcs capacities
au = dict(zip(zip(lanes_df['Origin Site'], lanes_df['Dest. Site']), lanes_df['Capacity (Trucks/Day)']))

mdl = pulp.LpProblem('MipEx Shortest Path', sense=pulp.LpMinimize)

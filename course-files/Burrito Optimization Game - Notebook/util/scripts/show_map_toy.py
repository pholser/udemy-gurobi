import plotly.graph_objects as go
from PIL import Image
import gurobipy as gp
import requests
import urllib.request
from io import BytesIO

def show_map_toy(demand, placed_trucks = []):
    """displays the Burrito Optimization map with labels for open truck locations, buildings with demand, and placed trucks [optional].  This is intended to be used in the Gurobi Days Intro to Modeling course.  This is modified for a small toy problem"""
    
    # Fix a bunch of data
    # Truck spots - set
    truck_spots = {'truck_spot_A', 'truck_spot_B'}

    # Truck spot coordinates - dictionary
    truck_coordinates = {
        'truck_spot_A': (156, 208),
        'truck_spot_B': (136,240),
        }
    truck_coordinates2 = {
        'spot_a': (156, 208),
        'spot_b': (136,240),
        }
    
    # Buildings with customer demands - set
    buildings = {'MILP_Mart', 'Toy_Problems_R_Us'}

    # Building names - dictionary
    building_names = {
        'MILP_Mart':         'MILP Mart',
        'Toy_Problems_R_Us': 'Toy Problems Я Us',
        }

    # Building coordiantes - dictionary
    building_coordinates = {
        'MILP_Mart':         (176,187),
        'Toy_Problems_R_Us': (165,250),
        }

    y_max = 550
    x_max = 500
    y_min = 0
    x_min = 0
    
    truck_spot_x = [value[0] for key, value in truck_coordinates.items()]
    truck_spot_y = [y_max - value[1] for key, value in truck_coordinates.items()]
    trucks = [key for key, value in truck_coordinates.items()]
    
    building_x = [value[0] for key, value in building_coordinates.items()]
    building_y = [y_max - value[1] for key, value in building_coordinates.items()]
    demand = [value for key, value in demand.items()]
    building_names = [value for key, value in building_names.items()]

    
    placed_trucks_orig = placed_trucks
    if placed_trucks:
        placed_truck_spot_x = [value[0] for key, value in truck_coordinates.items() if key in placed_trucks_orig]
        placed_truck_spot_y = [y_max - value[1] for key, value in truck_coordinates.items() if key in placed_trucks_orig]
        placed_trucks = [key for key, value in truck_coordinates.items() if key in placed_trucks_orig]
        placed_truck_spot_x = placed_truck_spot_x + [value[0] for key, value in truck_coordinates2.items() if key in placed_trucks_orig]
        placed_truck_spot_y = placed_truck_spot_y + [y_max - value[1] for key, value in truck_coordinates2.items() if key in placed_trucks_orig]
        placed_trucks = placed_trucks + [key for key, value in truck_coordinates2.items() if key in placed_trucks_orig]

    # Create figure
    url = 'https://raw.githubusercontent.com/Gurobi/modeling-examples/master/burrito_optimization_game/util/minimap.png'   
    response = requests.get(url)
    minimap = Image.open(BytesIO(response.content))
    fig = go.Figure()

    # Add trace for truck spots
    fig.add_trace(
        go.Scatter(x=truck_spot_x, y=truck_spot_y, 
                   hovertemplate=trucks, 
                   name="Open truck spots",
                   mode='markers',
                   marker_color='rgba(135, 206, 250, 0.0)',
                   marker_line_color='darkblue',
                   marker_line_width=3, 
                   marker_size=16
                   )
    )

    # Add trace for placed trucks
    if placed_trucks:
        fig.add_trace(
            go.Scatter(x=placed_truck_spot_x, y=placed_truck_spot_y, 
                       hovertemplate=placed_trucks, 
                       name="Truck added to the map",
                       mode='markers',
                       marker_color='darkblue',
                       marker_line_color='darkblue',
                       marker_line_width=3, 
                       marker_size=16
                       )
        )

    # Add trace for buildings
    fig.add_trace(
        go.Scatter(x=building_x, y=building_y, 
                   hovertemplate=building_names,
                   name="Buildings with customer demand",
                   mode='markers',
                   marker_color='red',
                   marker_opacity=0.5,
                   marker_line_width=0, 
                   marker_size=demand
                   )
    )

    # Add minimap image
    fig.add_layout_image(
            dict(
                source=minimap,
                xref="x",
                yref="y",
                x=0,
                y=550,
                sizex=500,
                sizey=550,
                sizing="stretch",
                opacity=0.9,
                layer="below")
    )

    # Set templates
    fig.update_layout(template="simple_white")
    
    if len(buildings)<=5:
        # I assume it's a toy problem, we will zoom in
        margin = 40
        x_min = min(min(truck_spot_x), min(building_x)) - margin
        x_max = max(max(truck_spot_x), max(building_x)) + margin
        y_min = min(min(truck_spot_y), min(building_y)) - margin
        y_max = max(max(truck_spot_y), max(building_y)) + margin
        fig.update_xaxes(range=[x_min, x_max], visible=False)
        fig.update_yaxes(range=[y_min,y_max], visible=False,
                    scaleanchor = "x",scaleratio = 1)
        
        # Add annotation for when no trucks are placed
        if placed_trucks==[]:
            ind = 0
            fig.add_annotation(x=truck_spot_x[ind]-2, y=truck_spot_y[ind]+2,
                text=f"A Burrito truck can be<br>placed in this<br>truck spot '{trucks[ind]}'.",
                showarrow=True,
                ax=-40,
                ay=-60,
                arrowhead=1,
                bgcolor="#FFFFFF",
                opacity=0.8)

            ind = len(building_x)-1
            fig.add_annotation(x=building_x[ind]+2, y=building_y[ind]-2,
                text=f"There are {demand[ind]}<br>customers who would <br>buy a burrito at <br>'{building_names[ind]}'.",
                showarrow=True,
                ax=100,
                ay=30,
                arrowhead=1,
                bgcolor="#FFFFFF",
                opacity=0.8)
    else:  
        fig.update_xaxes(range=[x_min, x_max], visible=False)
        fig.update_yaxes(range=[y_min, y_max], visible=False,
                        scaleanchor = "x",scaleratio = 1)
        
    fig.update_layout(showlegend=True)
    
    fig.update_layout(
        title="Burrito Optimization Game Map",
    )
    
    fig.show()
    

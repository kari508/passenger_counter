from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        os.getenv("DATABASE_URL"),
        cursor_factory=RealDictCursor
    )
    return conn

# Route & stop structure
stop_data = {
    "Down Valley": {
        "07:05–09:10": [
            "Placerville EB1", "Juniper Village EB1", "The Bivi EB1", "Fall Creek EB1", "Sawpit EB1", "Two Rivers EB1", "Vance Dr. EB1",
            "Lawson Hill Park and Ride EB1", "Eider Creek EB1", "Hillside EB1", "TMSHS EB1", "Courthouse EB1", "TMSHS WB1",
            "Hillside WB1", "Hillside 2 WB1", "Eider Creek WB1", "Lawson Hill Park and Ride WB1", "Two Rivers WB1", "Vance Dr. WB1",
            "Sawpit WB1", "Fall Creek WB1", "The Bivi WB1", "Juniper Village WB1", "Placerville WB1", "Juniper Village EB2",
            "The Bivi EB2", "Fall Creek EB2", "Sawpit EB2", "Two Rivers EB2", "Vance Dr. EB2", "Lawson Hill Park and Ride EB2",
            "Eider Creek EB2", "Hillside EB2", "TMSHS EB2", "Courthouse EB2"
        ],

        "11:30–13:00": [
            "Courthouse WB", "TMSHS WB", "Hillside WB", "Hillside 2 WB", "Eider Creek WB", "Upper Lawson Hill WB",
            "Lawson Hill Park and Ride WB", "Two Rivers WB", "Vance Dr. WB", "Sawpit WB", "Fall Creek WB", "The Bivi WB",
            "Juniper Village WB", "Placerville WB", "Juniper Village EB", "The Bivi EB", "Fall Creek EB", "Sawpit EB",
            "Two Rivers EB", "Vance Dr. EB", "Upper Lawson Hill EB", "Lawson Hill Park and Ride EB", "Eider Creek EB",
            "Hillside EB", "TMSHS EB", "Courthouse EB"
        ],

        "17:10–19:10": [
            "Courthouse WB1", "TMSHS WB1", "Hillside WB1", "Hillside 2 WB1", "Eider Creek WB1", "Lawson Hill Park and Ride WB1",
            "Two Rivers WB1", "Vance Dr. WB1", "Sawpit WB1", "Fall Creek WB1", "The Bivi WB1", "Juniper Village WB1", "Placerville EB1",
            "Juniper Village EB1", "The Bivi EB1", "Fall Creek EB1", "Sawpit EB1", "Two Rivers EB1", "Vance Dr. EB1",
            "Lawson Hill Park and Ride EB1", "Eider Creek EB1", "Hillside EB1", "TMSHS EB1", "Courthouse EB1", "TMSHS WB2",
            "Hillside WB2", "Hillside 2 WB2", "Eider Creek WB2", "Lawson Hill Park and Ride WB2", "Two Rivers WB2", "Vance Dr. WB2",
            "Sawpit WB2", "Fall Creek WB2", "The Bivi WB2", "Juniper Village WB2", "Placerville WB2"
        ]
    },

    "Lawson Hill": {
        "06:25–11:20": [
            "Town Park WB1", "Courthouse WB1", "TMSHS WB1", "Hillside WB1", "Hillside 2 WB1", "Eider Creek WB1", "Mountain School WB1",
            "Upper Lawson Hill WB1", "Mountain School EB1", "Lawson Hill Park and Ride EB1", "Eider Creek EB1", "Hillside EB1", "TMSHS EB1",
            "Courthouse EB1", "Town Park EB1",

            "Courthouse WB2", "TMSHS WB2", "Hillside WB2", "Hillside 2 WB2", "Eider Creek WB2", "Mountain School WB2",
            "Upper Lawson Hill WB2", "Mountain School EB2", "Lawson Hill Park and Ride EB2", "Eider Creek EB2", "Hillside EB2", "TMSHS EB2",
            "Courthouse EB2", "Town Park EB2",

            "Courthouse WB3", "TMSHS WB3", "Hillside WB3", "Hillside 2 WB3", "Eider Creek WB3", "Mountain School WB3",
            "Upper Lawson Hill WB3", "Mountain School EB3", "Lawson Hill Park and Ride EB3", "Eider Creek EB3", "Hillside EB3", "TMSHS EB3",
            "Courthouse EB3", "Town Park EB3",

            "Courthouse WB4", "TMSHS WB4", "Hillside WB4", "Hillside 2 WB4", "Eider Creek WB4", "Mountain School WB4",
            "Upper Lawson Hill WB4", "Mountain School EB4", "Lawson Hill Park and Ride EB4", "Eider Creek EB4", "Hillside EB4", "TMSHS EB4",
            "Courthouse EB4", "Town Park EB4",

            "Courthouse WB5", "TMSHS WB5", "Hillside WB5", "Hillside 2 WB5", "Eider Creek WB5", "Mountain School WB5",
            "Upper Lawson Hill WB5", "Mountain School EB5", "Lawson Hill Park and Ride EB5", "Eider Creek EB5", "Hillside EB5", "TMSHS EB5",
            "Courthouse EB5", "Town Park EB5",

             "Courthouse WB6", "TMSHS WB6", "Hillside WB6", "Hillside 2 WB6", "Eider Creek WB6", "Mountain School WB6",
            "Upper Lawson Hill WB6", "Mountain School EB6", "Lawson Hill Park and Ride EB6", "Eider Creek EB6", "Hillside EB6", "TMSHS EB6",
            "Courthouse EB6", "Town Park EB6"
        ],

        
        "14:25–20:25": [
            "Upper Lawson Hill EB1", "Mountain School EB1", "Lawson Hill Park and Ride EB1", "Eider Creek EB1", "Hillside EB1", "TMSHS EB1",
            "Courthouse EB1", "Town Park EB1",

            "Courthouse WB1", "TMSHS WB1", "Hillside WB1", "Hillside 2 WB1", "Eider Creek WB1", "Mountain School WB1",
            "Upper Lawson Hill WB1",

            "Mountain School EB2", "Lawson Hill Park and Ride EB2", "Eider Creek EB2", "Hillside EB2", "TMSHS EB2",
            "Courthouse EB2", "Town Park EB2",

            "Courthouse WB2", "TMSHS WB2", "Hillside WB2", "Hillside 2 WB2", "Eider Creek WB2", "Mountain School WB2",
            "Upper Lawson Hill WB2",

            "Mountain School EB3", "Lawson Hill Park and Ride EB3", "Eider Creek EB3", "Hillside EB3", "TMSHS EB3",
            "Courthouse EB3", "Town Park EB3",

            "Courthouse WB3", "TMSHS WB3", "Hillside WB3", "Hillside 2 WB3", "Eider Creek WB3", "Mountain School WB3",
            "Upper Lawson Hill WB3",

            "Mountain School EB4", "Lawson Hill Park and Ride EB4", "Eider Creek EB4", "Hillside EB4", "TMSHS EB4",
            "Courthouse EB4", "Town Park EB4",

            "Courthouse WB4", "TMSHS WB4", "Hillside WB4", "Hillside 2 WB4", "Eider Creek WB4", "Mountain School WB4",
            "Upper Lawson Hill WB4",

            "Mountain School EB5", "Lawson Hill Park and Ride EB5", "Eider Creek EB5", "Hillside EB5", "TMSHS EB5",
            "Courthouse EB5", "Town Park EB5",

            "Courthouse WB5", "TMSHS WB5", "Hillside WB5", "Hillside 2 WB5", "Eider Creek WB5", "Mountain School WB5",
            "Upper Lawson Hill WB5",

            "Mountain School EB5", "Lawson Hill Park and Ride EB6", "Eider Creek EB6", "Hillside EB6", "TMSHS EB6",
            "Courthouse EB6", "Town Park EB6"
        ],

        "20:25–22:40": [
            "Upper Lawson Hill EB1", "Mountain School EB1", "Lawson Hill Park and Ride EB1", "Eider Creek EB1", "Hillside EB1", "TMSHS EB1",
            "Courthouse EB1", "Town Park EB1",

            "Courthouse WB1", "TMSHS WB1", "Hillside WB1", "Hillside 2 WB1", "Eider Creek WB1", "Mountain School WB1",
            "Upper Lawson Hill WB1",

            "Mountain School EB2", "Lawson Hill Park and Ride EB2", "Eider Creek EB2", "Hillside EB2", "TMSHS EB2",
            "Courthouse EB2", "Town Park EB2",

            "Courthouse WB2", "TMSHS WB2", "Hillside WB2", "Hillside 2 WB2", "Eider Creek WB2", "Mountain School WB2",
            "Upper Lawson Hill WB2",

            "Mountain School EB3", "Lawson Hill Park and Ride EB3", "Eider Creek EB3", "Hillside EB3", "TMSHS EB3",
            "Courthouse EB3", "Town Park EB3",

            "Town Park WB3", "Courthouse WB3", "TMSHS WB3", "Hillside WB3", "Hillside 2 WB3", "Eider Creek WB3", "Mountain School WB3",
            "Upper Lawson Hill WB3"
        ],
    },
    
    "Lawson Hill Mountain Village": {
        "07:35–09:35": [
        "Upper Lawson Hill EB1", "Mountain School EB1", "Lawson Hill Park and Ride EB1", "VCA EB1", "Market Plaza EB1", "Blue Mesa EB1", "Centrum EB1",
        "Blue Mesa WB1", "Market Plaza WB1", "VCA WB1", "Mountain School WB1", "Upper Lawson Hill WB1",

        "Mountain School EB2", "Lawson Hill Park and Ride EB2", "VCA EB2", "Market Plaza EB2", "Blue Mesa EB2", "Centrum EB2",
        "Blue Mesa WB2", "Market Plaza WB2", "VCA WB2", "Mountain School WB2", "Upper Lawson Hill WB2",

        "Mountain School EB3", "Lawson Hill Park and Ride EB3", "VCA EB3", "Market Plaza EB3", "Blue Mesa EB3", "Centrum EB3",
        "Blue Mesa WB3", "Market Plaza WB3", "VCA WB3", "Mountain School WB3", "Upper Lawson Hill WB3"
        ],

    
        "16:40–18:40": [
            "Upper Lawson Hill EB1", "Mountain School EB1", "Lawson Hill Park and Ride EB1", "VCA EB1", "Market Plaza EB1", "Blue Mesa EB1", "Centrum EB1",
            "Blue Mesa WB1", "Market Plaza WB1", "VCA WB1", "Mountain School WB1", "Upper Lawson Hill WB1",

            "Mountain School EB2", "Lawson Hill Park and Ride EB2", "VCA EB2", "Market Plaza EB2", "Blue Mesa EB2", "Centrum EB2",
            "Blue Mesa WB2", "Market Plaza WB2", "VCA WB2", "Mountain School WB2", "Upper Lawson Hill WB2",

            "Mountain School EB3", "Lawson Hill Park and Ride EB3", "VCA EB3", "Market Plaza EB3", "Blue Mesa EB3", "Centrum EB3",
            "Blue Mesa WB3", "Market Plaza WB3", "VCA WB3", "Mountain School WB3", "Upper Lawson Hill WB3"
        ]     
    },

    "Montrose": {
        "06:00–08:00": [
            "North 2nd and Cascade", "Ridgway", "TMSHS", "Courthouse", "Town Park"
        ],
        "17:00–19:00": [
            "Town Park", "Courthouse", "TMSHS", "Ridgway", "North 2nd and Cascade"
        ]
    },
    
    "Norwood": {
        "06:55–08:05": [
            "Norwood Fairgrounds", "Pine St.", "Market St.", "Norwood Park and Ride", "Lower Placerville",
            "Placerville", "Juniper Village", "The Bivi", "Fall Creek", "Sawpit", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park"
        ],
        "09:45–12:15": [
            "Town Park WB", "Courthouse WB", "TMSHS WB", "Hillside WB", "Hillside 2 WB", "Eider Creek WB", "Lawson Hill Park and Ride WB",
            "Two Rivers WB", "Vance Dr. WB", "Sawpit WB", "Fall Creek WB", "The Bivi WB", "Juniper Village WB", "Placerville WB",
            "Lower Placerville WB", "Norwood Park and Ride WB", "Market St. WB", "Pine St. WB", "Norwood Fairgrounds EB",
            "Pine St. EB", "Market St. EB", "Norwood Park and Ride EB", "Lower Placerville EB", "Placerville EB",
            "Juniper Village EB", "The Bivi EB", "Fall Creek EB", "Sawpit EB", "Two Rivers EB", "Vance Dr. EB",
            "Lawson Hill Park and Ride EB", "Eider Creek EB", "Hillside EB", "TMSHS EB", "Courthouse EB", "Town Park EB"
        ],
        "17:15–18:20": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Sawpit", "Fall Creek",
            "The Bivi", "Juniper Village", "Placerville", "Lower Placerville", "Norwood Park and Ride",
            "Market St.", "Pine St.", "Norwood Fairgrounds"
        ],
        "07:25–08:30": [
            "Norwood Fairgrounds", "Pine St.", "Market St.", "Norwood Park and Ride", "Lower Placerville",
            "Placerville", "Juniper Village", "The Bivi", "Fall Creek", "Sawpit", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
        ],
        "17:00–18:05": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Lawson Hill Park and Ride",
            "Sawpit", "Fall Creek", "The Bivi", "Juniper Village", "Placerville", "Lower Placerville",
            "Norwood Park and Ride", "Market St.", "Pine St.", "Norwood Fairgrounds"
        
        ],
        "23:30–24:45": [
            "Town Park WB", "Courthouse WB", "TMSHS WB", "Hillside WB", "Hillside 2 WB", "Eider Creek WB", "Lawson Hill Park and Ride WB",
            "Two Rivers WB", "Vance Dr. WB", "Sawpit WB", "Fall Creek WB", "The Bivi WB", "Juniper Village WB", "Placerville WB",
            "Lower Placerville WB", "Norwood Park and Ride WB", "Market St. WB", "Pine St. WB", "Norwood Fairgrounds EB",
        
        ]
    },
    
    "Nucla/Naturita": {
        "06:45–08:30": [
            "Nucla North", "Nucla Town Park", "Naturita", "Redvale", "Norwood Fairgrounds", "Pine St.",
            "Market St.", "Norwood Park and Ride", "Lower Placerville", "Placerville", "Juniper Village",
            "The Bivi", "Fall Creek", "Sawpit", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park"
        ],
        "17:00–18:45": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Lawson Hill Park and Ride",
            "Sawpit", "Fall Creek", "The Bivi", "Juniper Village", "Placerville", "Lower Placerville",
            "Norwood Park and Ride", "Market St.", "Pine St.", "Norwood Fairgrounds", "Redvale", "Naturita",
            "Nucla Town Park", "Nucla North"
        ]
    },
    
    "Rico": {
        "07:00–07:45": [
            "Enterprise Bar", "San Bernardo", "Eider Creek", "TMSHS", "Courthouse"
        ],
        "17:15–18:10": [
            "Courthouse", "TMSHS", "Eider Creek", "San Bernardo", "Enterprise Bar"
        ]
    },

    "Offseason Bus A": {
        "05:55–11:20": [
    # Loop 1
            "Upper Lawson Hill VB1", "Mountain School VB1", "Lawson Hill Park and Ride VB1", "Meadows P.O. VB1", "Big Billies VB1", "The Boulders VB1", "VCA VB1",
            "Market Plaza VB1", "Blue Mesa VB1", "Centrum VB1",

            "Blue Mesa TB1", "Market Plaza TB1", "VCA TB1", "Meadows P.O. TB1", "Big Billies TB1", "The Boulders TB1",
            "Mountain School TB1", "Upper Lawson Hill TB1", "Lawson Hill Park and Ride TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1",
            "Courthouse TB1", "Town Park TB1",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "Mountain School VB2",
            "Upper Lawson Hill VB2", "Lawson Hill Park and Ride VB2", "Meadows P.O. VB2", "Big Billies VB2", "The Boulders VB2", "VCA VB2",
            "Market Plaza VB2", "Blue Mesa VB2",

            "Centrum TB2", "Blue Mesa TB2", "Market Plaza TB2", "VCA TB2", "Meadows P.O. TB2", "Big Billies TB2", "The Boulders TB2",
            "Mountain School TB2", "Upper Lawson Hill TB2", "Lawson Hill Park and Ride TB2", "Eider Creek TB2", "Hillside TB2",
            "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 3
            "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "Mountain School VB3",
            "Upper Lawson Hill VB3", "Lawson Hill Park and Ride VB3", "Meadows P.O. VB3", "Big Billies VB3", "The Boulders VB3", "VCA VB3",
            "Market Plaza VB3", "Blue Mesa VB3", "Centrum VB3",

            "Blue Mesa TB3", "Market Plaza TB3", "VCA TB3", "Meadows P.O. TB3", "Big Billies TB3", "The Boulders TB3", 
            "Mountain School TB3", "Upper Lawson Hill TB3", "Lawson Hill Park and Ride TB3", "Eider Creek TB3", "Hillside TB3",
            "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Partial Loop 4 (if needed, can continue to TB4 if more stops)
            "Courthouse VB4", "TMSHS VB4", "Hillside VB4", "Hillside 2 VB4", "Eider Creek VB4", "Mountain School VB4",
            "Upper Lawson Hill VB4", "Lawson Hill Park and Ride VB4", "Meadows P.O. VB4"

        ],
        
        "11:25–17:25": [
    # Loop 1
            "Upper Lawson Hill TB1", "Lawson Hill Park and Ride TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1",
            "Town Park TB1",

            "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "Mountain School VB1",
            "Upper Lawson Hill VB1", "Lawson Hill Park and Ride VB1", "Meadows P.O. VB1", "Big Billies VB1", "The Boulders VB1", "VCA VB1",
            "Market Plaza VB1", "Blue Mesa VB1", 

            "Centrum TB1", "Blue Mesa TB2", "Market Plaza TB2", "VCA TB2", "Meadows P.O. TB2", "Big Billies TB2", "The Boulders TB2",
            "Mountain School TB2", "Upper Lawson Hill TB2", "Lawson Hill Park and Ride TB2", "Eider Creek TB2", "Hillside TB2",
            "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "Mountain School VB2",
            "Upper Lawson Hill VB2", "Lawson Hill Park and Ride VB2", "Meadows P.O. VB2", "Big Billies VB2", "The Boulders VB2", "VCA VB2",
            "Market Plaza VB2", "Blue Mesa VB2", "Centrum VB2",

            "Blue Mesa TB3", "Market Plaza TB3", "VCA TB3", "Meadows P.O. TB3", "Big Billies TB3", "The Boulders TB3",
            "Mountain School TB3", "Upper Lawson Hill TB3", "Lawson Hill Park and Ride TB3", "Eider Creek TB3", "Hillside TB3",
            "TMSHS TB3", "Courthouse TB3", 

            # Loop 3
            "Town Park VB3","Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "Mountain School VB3",
            "Upper Lawson Hill VB3", "Lawson Hill Park and Ride VB3", "Meadows P.O. VB3", "Big Billies VB3", "The Boulders VB3", "VCA VB3",
            "Market Plaza VB3", "Blue Mesa VB3", "Centrum VB3", "Blue Mesa VB4", "Market Plaza VB4", "VCA VB4", "Meadows P.O. VB4"
        ],

        
        "17:30–23:08": [
    # Loop 1
            "Upper Lawson Hill TB1", "Lawson Hill Park and Ride TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1",
            "Town Park TB1",

            "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "Mountain School VB1",
            "Upper Lawson Hill VB1", "Lawson Hill Park and Ride VB1", "Meadows P.O. VB1", "Big Billies VB1", "The Boulders VB1", "VCA VB1",
            "Market Plaza VB1", "Blue Mesa VB1", "Centrum VB1",

            "Blue Mesa TB2", "Market Plaza TB2", "VCA TB2", "Meadows P.O. TB2", "Big Billies TB2", "The Boulders TB2",
            "Mountain School TB2", "Upper Lawson Hill TB2", "Lawson Hill Park and Ride TB2", "Eider Creek TB2", "Hillside TB2",
            "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "Mountain School VB2",
            "Upper Lawson Hill VB2", "Lawson Hill Park and Ride VB2", "Meadows P.O. VB2", "Big Billies VB2", "The Boulders VB2", "VCA VB2",
            "Market Plaza VB2", "Blue Mesa VB2", "Centrum VB2",

            "Blue Mesa TB3", "Market Plaza TB3", "VCA TB3", "Meadows P.O. TB3", "Big Billies TB3", "The Boulders TB3",
            "Mountain School TB3", "Upper Lawson Hill TB3", "Lawson Hill Park and Ride TB3", "Eider Creek TB3", "Hillside TB3",
            "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Loop 3
            "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "Mountain School VB3",
            "Upper Lawson Hill VB3", "Lawson Hill Park and Ride VB3", "Meadows P.O. VB3", "Big Billies VB3", "The Boulders VB3", "VCA VB3",
            "Market Plaza VB3", "Blue Mesa VB3", "Centrum VB3", "Blue Mesa VB4", "Market Plaza VB4", "VCA VB4", "Meadows P.O. VB4"
        ]
       
    },


    "Offseason Bus B": {
        "06:55–11:51": [
    # Loop 1
            "Upper Lawson Hill TB1", "Lawson Hill Park and Ride TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1",
            "Town Park TB1",

            "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "Mountain School VB1",
            "Upper Lawson Hill VB1", "Lawson Hill Park and Ride VB1", "Meadows P.O. VB1", "Big Billies VB1", "The Boulders VB1", "VCA VB1",
            "Market Plaza VB1", "Blue Mesa VB1", "Centrum VB1",

            "Blue Mesa TB2", "Market Plaza TB2", "VCA TB2", "Meadows P.O. TB2", "Big Billies TB2", "The Boulders TB2",
            "Mountain School TB2", "Upper Lawson Hill TB2", "Lawson Hill Park and Ride TB2", "Eider Creek TB2", "Hillside TB2",
            "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "Mountain School VB2",
            "Upper Lawson Hill VB2", "Lawson Hill Park and Ride VB2", "Meadows P.O. VB2", "Big Billies VB2", "The Boulders VB2", "VCA VB2",
            "Market Plaza VB2", "Blue Mesa VB2", "Centrum VB2",

            "Blue Mesa TB3", "Market Plaza TB3", "VCA TB3", "Meadows P.O. TB3", "Big Billies TB3", "The Boulders TB3",
            "Mountain School TB3", "Upper Lawson Hill TB3", "Lawson Hill Park and Ride TB3", "Eider Creek TB3", "Hillside TB3",
            "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Loop 3
            "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "Mountain School VB3",
            "Upper Lawson Hill VB3", "Lawson Hill Park and Ride VB3", "Meadows P.O. VB3", "Big Billies VB3", "The Boulders VB3", "VCA VB3",
            "Market Plaza VB3", "Blue Mesa VB3", "Centrum VB3",

            "Blue Mesa VB4", "Market Plaza VB4", "VCA VB4", "Meadows P.O. VB4", "Big Billies VB4", "Mountain School VB4"
        ],

        
        "12:10–17:56": [
    # Loop 1
            "Upper Lawson Hill TB1", "Lawson Hill Park and Ride TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1",
            "Town Park TB1",

            "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "Mountain School VB1",
            "Upper Lawson Hill VB1", "Lawson Hill Park and Ride VB1", "Meadows P.O. VB1", "Big Billies VB1", "The Boulders VB1", "VCA VB1",
            "Market Plaza VB1", "Blue Mesa VB1", "Centrum VB1",

            "Blue Mesa TB2", "Market Plaza TB2", "VCA TB2", "Meadows P.O. TB2", "Big Billies TB2", "The Boulders TB2",
            "Mountain School TB2", "Upper Lawson Hill TB2", "Lawson Hill Park and Ride TB2", "Eider Creek TB2", "Hillside TB2",
            "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "Mountain School VB2",
            "Upper Lawson Hill VB2", "Lawson Hill Park and Ride VB2", "Meadows P.O. VB2", "Big Billies VB2", "The Boulders VB2", "VCA VB2",
            "Market Plaza VB2", "Blue Mesa VB2", "Centrum VB2",

            "Blue Mesa TB3", "Market Plaza TB3", "VCA TB3", "Meadows P.O. TB3", "Big Billies TB3", "The Boulders TB3",
            "Mountain School TB3", "Upper Lawson Hill TB3", "Lawson Hill Park and Ride TB3", "Eider Creek TB3", "Hillside TB3",
            "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Loop 3
            "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "Mountain School VB3",
            "Upper Lawson Hill VB3", "Lawson Hill Park and Ride VB3", "Meadows P.O. VB3", "Big Billies VB3", "The Boulders VB3", "VCA VB3",
            "Market Plaza VB3", "Blue Mesa VB3", "Centrum VB3",

            "Blue Mesa TB4", "Market Plaza TB4", "VCA TB4", "Meadows P.O. TB4"
        ],

        "18:15–24:01": [
            # Loop 1
            "Upper Lawson Hill TB1", "Lawson Hill Park and Ride TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1",
            "Town Park TB1",

            "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "Mountain School VB1",
            "Upper Lawson Hill VB1", "Lawson Hill Park and Ride VB1", "Meadows P.O. VB1", "Big Billies VB1", "The Boulders VB1", "VCA VB1",
            "Market Plaza VB1", "Blue Mesa VB1", "Centrum VB1",

            "Blue Mesa TB2", "Market Plaza TB2", "VCA TB2", "Meadows P.O. TB2", "Big Billies TB2", "The Boulders TB2",
            "Mountain School TB2", "Upper Lawson Hill TB2", "Lawson Hill Park and Ride TB2", "Eider Creek TB2", "Hillside TB2",
            "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "Mountain School VB2",
            "Upper Lawson Hill VB2", "Lawson Hill Park and Ride VB2", "Meadows P.O. VB2", "Big Billies VB2", "The Boulders VB2", "VCA VB2",
            "Market Plaza VB2", "Blue Mesa VB2", "Centrum VB2",

            "Blue Mesa TB3", "Market Plaza TB3", "VCA TB3", "Meadows P.O. TB3", "Big Billies TB3", "The Boulders TB3",
            "Mountain School TB3", "Upper Lawson Hill TB3", "Lawson Hill Park and Ride TB3", "Eider Creek TB3", "Hillside TB3",
            "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Loop 3
            "Town Park VB3", "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "Mountain School VB3",
            "Upper Lawson Hill VB3", "Lawson Hill Park and Ride VB3", "Meadows P.O. VB3", "Big Billies VB3", "The Boulders VB3", "VCA VB3",
            "Market Plaza VB3", "Blue Mesa VB3", "Centrum VB3",

            "Blue Mesa TB4", "Market Plaza TB4", "VCA TB4", "Eider Creek TB4", "Hillside TB4", "TMSHS TB4", "Courthouse TB4", "Town Park TB4"
        ]
      
    },

    "Offseason Express": {
        "06:15–11:40": [
            # Loop 1
            "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "VCA VB1", "Market Plaza VB1",
            "Blue Mesa VB1",

            "Market Plaza TB1", "VCA TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1", "Town Park TB1",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "VCA VB2", "Market Plaza VB2", "Blue Mesa VB2",

            "Market Plaza TB2", "VCA TB2", "Eider Creek TB2", "Hillside TB2", "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 3
            "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "VCA VB3", "Market Plaza VB3", "Blue Mesa VB3",

            "Market Plaza TB3", "VCA TB3", "Eider Creek TB3", "Hillside TB3", "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Loop 4
            "Courthouse VB4", "TMSHS VB4", "Hillside VB4", "Hillside 2 VB4", "Eider Creek VB4", "VCA VB4", "Market Plaza VB4", "Blue Mesa VB4",

            "Market Plaza TB4", "VCA TB4", "Eider Creek TB4", "Hillside TB4", "TMSHS TB4", "Courthouse TB4", "Town Park TB4",

            # Loop 5
            "Courthouse VB5", "TMSHS VB5", "Hillside VB5", "Hillside 2 VB5", "Eider Creek VB5", "VCA VB5", "Market Plaza VB5", "Blue Mesa VB5",

            "Market Plaza TB5", "VCA TB5", "Eider Creek TB5", "Hillside TB5", "TMSHS TB5", "Courthouse TB5", "Town Park TB5",

            # Loop 6
            "Courthouse VB6", "TMSHS VB6", "Hillside VB6", "Hillside 2 VB6", "Eider Creek VB6", "VCA VB6", "Market Plaza VB6", "Blue Mesa VB6",

            "Market Plaza TB6", "VCA TB6", "Eider Creek TB6", "Hillside TB6", "TMSHS TB6", "Courthouse TB6", "Town Park TB6"
        ],

       
        "11:50–19:05": [
    # Loop 1
            "Town Park VB1", "Courthouse VB1", "TMSHS VB1", "Hillside VB1", "Hillside 2 VB1", "Eider Creek VB1", "VCA VB1", "Market Plaza VB1", "Blue Mesa VB1",

            "Market Plaza TB1b", "VCA TB1", "Eider Creek TB1", "Hillside TB1", "TMSHS TB1", "Courthouse TB1", "Town Park TB1",

            # Loop 2
            "Courthouse VB2", "TMSHS VB2", "Hillside VB2", "Hillside 2 VB2", "Eider Creek VB2", "VCA VB2", "Market Plaza VB2", "Blue Mesa VB2",

            "Market Plaza TB2", "VCA TB2", "Eider Creek TB2", "Hillside TB2", "TMSHS TB2", "Courthouse TB2", "Town Park TB2",

            # Loop 3
            "Courthouse VB3", "TMSHS VB3", "Hillside VB3", "Hillside 2 VB3", "Eider Creek VB3", "VCA VB3", "Market Plaza VB3", "Blue Mesa VB3",

            "Market Plaza TB3", "VCA TB3", "Eider Creek TB3", "Hillside TB3", "TMSHS TB3", "Courthouse TB3", "Town Park TB3",

            # Loop 4
            "Town Park VB4", "Courthouse VB4", "TMSHS VB4", "Hillside VB4", "Hillside 2 VB4", "Eider Creek VB4", "VCA VB4", "Market Plaza VB4", "Blue Mesa VB4",

            "Market Plaza TB4", "VCA TB4", "Eider Creek TB4", "Hillside TB4", "TMSHS TB4", "Courthouse TB4", "Town Park TB4",

            # Loop 5
            "Courthouse VB5", "TMSHS VB5", "Hillside VB5", "Hillside 2 VB5", "Eider Creek VB5", "VCA VB5", "Market Plaza VB5", "Blue Mesa VB5",

            "Blue Mesa TB5", "Market Plaza TB5", "VCA TB5", "Eider Creek TB5", "Hillside TB5", "TMSHS TB5", "Courthouse TB5", "Town Park TB5",

            # Loop 6
            "Courthouse VB6", "TMSHS VB6", "Hillside VB6", "Hillside 2 VB6", "Eider Creek VB6", "VCA VB6", "Market Plaza VB6", "Blue Mesa VB6",

            "Market Plaza TB6", "VCA TB6", "Eider Creek TB6", "Hillside TB6", "TMSHS TB6", "Courthouse TB6", "Town Park TB6",

            # Loop 7
            "Courthouse VB7", "TMSHS VB7", "Hillside VB7", "Hillside 2 VB7", "Eider Creek VB7", "VCA VB7", "Market Plaza VB7", "Blue Mesa VB7",

            "Market Plaza TB7", "VCA TB7", "Eider Creek TB7", "Hillside TB7", "TMSHS TB7", "Courthouse TB7", "Town Park TB7"
      ]  # closes the final list
    }  # closes "Offseason Express"
    }  # closes stop_data = { ... }




@app.route("/", methods=["GET", "HEAD"])
def index():
    if request.method == "HEAD":
        return "", 200

    selected_route = request.args.get("route", "")
    selected_time_block = request.args.get("time_block", "")
    selected_stop = request.args.get("stop", "")
    submitted = request.args.get("submitted", "false")

    return render_template(
        "index.html",
        stop_data=stop_data,
        selected_route=selected_route,
        selected_time_block=selected_time_block,
        selected_stop=selected_stop,
        submitted=submitted
    )

@app.route("/submit", methods=["POST"])
def submit():
    # Basic trip details
    route = request.form.get("route")
    time_block = request.form.get("time_block")
    stop = request.form.get("stop")
    stop_index = int(request.form.get("stop_index", 0))
    direction = request.form.get("direction", "forward")  # "forward" or "back"

    # If direction is "back", skip logging and go to the previous stop
    if direction == "back":
        new_index = max(0, stop_index - 1)
        prev_stop = stop_data.get(route, {}).get(time_block, [])[new_index]
        return redirect(url_for(
            "index",
            route=route,
            time_block=time_block,
            stop=prev_stop,
            stop_index=new_index,
            submitted="false"
        ))

    # Passenger counts
    on_count = int(request.form.get("on_count", 0))
    off_count = int(request.form.get("off_count", 0))
    student_on = int(request.form.get("student_on", 0))
    student_off = int(request.form.get("student_off", 0))

    # Payment details
    cash_collected = float(request.form.get("cash_collected") or 0)
    tickets_collected = float(request.form.get("tickets_collected") or 0)
    ticket_books_sold = float(request.form.get("ticket_books_sold") or 0)
    credit = float(request.form.get("credit") or 0)

    # Timestamp
    from datetime import datetime
    import pytz
    mountain_time = pytz.timezone("America/Denver")
    now = datetime.now(mountain_time)
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Insert into DB
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO passenger_logs
    (date, time, route, time_block, stop, passengers_on, passengers_off,
     student_on, student_off, cash_collected, tickets_collected,
     ticket_books_sold, credit, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())
""", (
    date_str, time_str, route, time_block, stop,
    on_count, off_count,
    student_on, student_off,
    cash_collected, tickets_collected, ticket_books_sold, credit
))


    conn.commit()
    cur.close()
    conn.close()

    # Forward navigation
    stops = stop_data.get(route, {}).get(time_block, [])
    if stop_index + 1 < len(stops):
        next_stop = stops[stop_index + 1]
        return redirect(url_for(
            "index",
            route=route,
            time_block=time_block,
            stop=next_stop,
            stop_index=stop_index + 1,
            submitted="true"
        ))
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    print("Launching SMART Passenger Counter...")
    app.run(debug=True, host="0.0.0.0")




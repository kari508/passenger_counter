from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Route & stop structure
stop_data = {
    "Down Valley": {
        "07:05–09:10": [
            "Placerville", "Juniper Village", "The Bivi", "Fall Creek", "Sawpit", "Two Rivers", "Vance Dr.",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "TMSHS",
            "Hillside", "Hillside 2", "Eider Creek", "Lawson Hill Park and Ride", "Two Rivers", "Vance Dr.",
            "Sawpit", "Fall Creek", "The Bivi", "Juniper Village", "Placerville", "Juniper Village",
            "The Bivi", "Fall Creek", "Sawpit", "Two Rivers", "Vance Dr.", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse"
        ],
        "11:30–13:00": [
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Two Rivers", "Vance Dr.", "Sawpit", "Fall Creek", "The Bivi",
            "Juniper Village", "Placerville", "Juniper Village", "The Bivi", "Fall Creek", "Sawpit",
            "Two Rivers", "Vance Dr.", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse"
        ],
        "17:10–19:10": [
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Lawson Hill Park and Ride",
            "Two Rivers", "Vance Dr.", "Sawpit", "Fall Creek", "The Bivi", "Juniper Village", "Placerville",
            "Juniper Village", "The Bivi", "Fall Creek", "Sawpit", "Two Rivers", "Vance Dr.",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "TMSHS",
            "Hillside", "Hillside 2", "Eider Creek", "Lawson Hill Park and Ride", "Two Rivers", "Vance Dr.",
            "Sawpit", "Fall Creek", "The Bivi", "Juniper Village", "Placerville"
        ]
    },

    "Lawson Hill": {
        "06:25–11:20": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS",
            "Hillside", "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill"
        ],
        "14:25–20:25": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS",
            "Hillside", "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS",
            "Hillside", "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill"
        ],
        "20:25–22:40": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS",
            "Hillside", "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill"
        ]
    },
 
    "Lawson Hill Mountain Village": {
        "07:35–09:35": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Mountain School", "Upper Lawson Hill"
        ],
        "16:40–18:40": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Mountain School", "Upper Lawson Hill"
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
        "06:55–08:30": [
            "Norwood Fairgrounds", "Pine St.", "Market St.", "Norwood Park and Ride", "Lower Placerville",
            "Placerville", "Juniper Village", "The Bivi", "Fall Creek", "Sawpit", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park"
        ],
        "09:45–12:15": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Lawson Hill Park and Ride",
            "Two Rivers", "Vance Dr.", "Sawpit", "Fall Creek", "The Bivi", "Juniper Village", "Placerville",
            "Lower Placerville", "Norwood Park and Ride", "Market St.", "Pine St.", "Norwood Fairgrounds",
            "Pine St.", "Market St.", "Norwood Park and Ride", "Lower Placerville", "Placerville",
            "Juniper Village", "The Bivi", "Fall Creek", "Sawpit", "Two Rivers", "Vance Dr.",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
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
        ]
    },
    "Nucla/Naturita": {
        "06:55–08:30": [
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
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies",
            "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA",
            "Meadows P.O.", "Big Billies", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O."
        ],
        "11:25–17:25": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.",
            "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza",
            "VCA", "Meadows P.O.", "Big Billies", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies", "The Boulders", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O."
        ],
        "17:30–23:08": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.",
            "Big Billies", "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies", "Mountain School", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse",
            "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza",
            "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.",
            "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa",
            "Market Plaza", "VCA", "Meadows P.O."
        ]
    },

    "Offseason Bus B": {
        "06:55–11:51": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.",
            "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza",
            "VCA", "Meadows P.O.", "Big Billies", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa",
            "Market Plaza", "VCA", "Meadows P.O.", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.",
            "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza",
            "VCA", "Meadows P.O.", "Big Billies", "Mountain School"
        ],
        "12:10–17:56": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.",
            "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza",
            "VCA", "Meadows P.O.", "Big Billies", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa",
            "Market Plaza", "VCA", "Meadows P.O.", "Big Billies", "The Boulders", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O."
        ],
        "18:15–24:01": [
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School",
            "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA",
            "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.",
            "Big Billies", "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride",
            "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum",
            "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies", "Mountain School", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse",
            "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "Mountain School", "Upper Lawson Hill",
            "Lawson Hill Park and Ride", "Meadows P.O.", "Big Billies", "The Boulders", "VCA", "Market Plaza",
            "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza", "VCA", "Meadows P.O.", "Big Billies",
            "The Boulders", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "Mountain School", "Upper Lawson Hill", "Lawson Hill Park and Ride", "Meadows P.O.",
            "Big Billies", "The Boulders", "VCA", "Market Plaza", "Blue Mesa", "Centrum", "Blue Mesa", "Market Plaza",
            "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
        ]
    },

    "Offseason Express": {
        "06:15–11:40": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa",
            "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse",
            "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza",
            "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA",
            "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
        ],
        "11:50–19:05": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa",
            "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse",
            "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza",
            "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA",
            "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa",
            "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
        ]
    },
    
    "Offseason Express": {
        "06:15–11:40": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa",
            "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse",
            "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza",
            "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA",
            "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
        ],
        "11:50–19:05": [
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa",
            "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse",
            "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza",
            "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside",
            "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek",
            "Hillside", "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2",
            "Eider Creek", "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside",
            "TMSHS", "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek",
            "VCA", "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS",
            "Courthouse", "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA",
            "Market Plaza", "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse",
            "Town Park", "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza",
            "Blue Mesa", "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park",
            "Courthouse", "TMSHS", "Hillside", "Hillside 2", "Eider Creek", "VCA", "Market Plaza", "Blue Mesa",
            "Market Plaza", "VCA", "Eider Creek", "Hillside", "TMSHS", "Courthouse", "Town Park"
        ]
    }
}



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
        stop_data=stop_data,  # <-- this is the important addition
        selected_route=selected_route,
        selected_time_block=selected_time_block,
        selected_stop=selected_stop,
        submitted=submitted
    )


@app.route("/submit", methods=["POST"])
def submit():
    # Basic data
    route = request.form.get("route")
    time_block = request.form.get("time_block")
    stop = request.form.get("stop")
    on_count = int(request.form.get("on_count", 0))
    off_count = int(request.form.get("off_count", 0))

    # New numeric payment fields
    ticket_books_sold = int(request.form.get("ticket_books_sold", 0))
    cash_collected = int(request.form.get("cash_collected", 0))
    tickets_collected = int(request.form.get("tickets_collected", 0))
    credit = int(request.form.get("credit", 0))

    # Timestamp
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    full_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Log entry
    new_entry = {
        "Date": date_str,
        "Time": time_str,
        "Route": route,
        "Time Block": time_block,
        "Stop": stop,
        "Passengers On": on_count,
        "Passengers Off": off_count,
        "Ticket Books Sold": ticket_books_sold,
        "Cash Collected": cash_collected,
        "Tickets Collected": tickets_collected,
        "Credit": credit,
        "Timestamp": full_timestamp
    }

    # Save to daily log
    os.makedirs("logs", exist_ok=True)
    daily_file = f"logs/{date_str}.xlsx"
    if not os.path.exists(daily_file):
        df_daily = pd.DataFrame([new_entry])
    else:
        df_daily = pd.read_excel(daily_file)
        df_daily = pd.concat([df_daily, pd.DataFrame([new_entry])], ignore_index=True)
    df_daily.to_excel(daily_file, index=False)

    # Save to monthly log
    monthly_file = "passenger_log.xlsx"
    if not os.path.exists(monthly_file):
        df_monthly = pd.DataFrame([new_entry])
    else:
        df_monthly = pd.read_excel(monthly_file)
        df_monthly = pd.concat([df_monthly, pd.DataFrame([new_entry])], ignore_index=True)
    df_monthly.to_excel(monthly_file, index=False)

    # Move to next stop
    next_stop = ""
    try:
        stops = stop_data[route][time_block]
        current_index = stops.index(stop)
        if current_index + 1 < len(stops):
            next_stop = stops[current_index + 1]
    except Exception as e:
        print(f"Stop progression error: {e}")

    return redirect(url_for(
        "index",
        route=route,
        time_block=time_block,
        stop=next_stop,
        submitted="true"
    ))

@app.route("/download")
def download():
    return send_file("passenger_log.xlsx", as_attachment=True)

if __name__ == "__main__":
    print("Launching SMART Passenger Counter...")
    app.run(debug=True, host="0.0.0.0")








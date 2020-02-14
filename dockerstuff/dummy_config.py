SG_CONF = {"SGconf": {
        "group":1,
        "deviceID": "RPI",
        "targetIP": "http://13.55.147.2/report",

        "signal": "any",
        "commType": "forward"
    }
}

AUS_CONF= {
        "AUSoff" : {
        "group":1,
        "deviceID":"RPI",
        "signal":"OFF",
        "commType":"device",
        "sayThis":"OFF"
        
    },
    "AUSon" : {
        "group":1,
        "deviceID":"RPI",
        "signal":"ON",
        "commType":"device",
        "sayThis":"ON"

    }
}

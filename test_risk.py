from risk_analyzer import analyze_risk


sample_data = {

    "url":{
        "safe":False
    },

    "image":{
        "fake":True
    }

}


result = analyze_risk(sample_data)

print(result)
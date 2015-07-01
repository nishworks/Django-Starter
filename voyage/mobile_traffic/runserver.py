from flask import Flask, jsonify
from flask.ext.cors import CORS, cross_origin
from flask.ext import restful
from utils import *
from main import androidStat, iosStat


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = restful.Api(app)


class xAndroidAPI(restful.Resource):

    @cross_origin()
    def get(self, xosversion,global_threshold, threshold, osmax, osmin):
        
        if xosversion not in ['x','xx','xxx']:
            x,xx,xxx = processOsVersion(xosversion)
            if x is None:
                return jsonify({"Error": "Please specify a xOSversion x, xx, xxx, 5, 5.1, 5.1.2"})
            osmax = x
            osmin = x
            print "x %s" % x
        try:
            threshold = float(threshold)
            global_threshold = float(global_threshold)
        except:
            return jsonify({"Error": "Please specify a valid threshold value like 1,1.3,1.0"})
        print "os_version: %s"% xosversion
        roundby = 3
        try:
            roundby = int(roundby)
        except:
            return jsonify({"Error": "Please specify a valid roundBy value like 1,1.3,1.0"})

        result = androidStat.xStats(xosversion,global_threshold,threshold, roundby,osmax,osmin)
        
        if result == None:
            return jsonify({"Error": "No stats found for this os version"})

        return jsonify(**result)

class IosAPI(restful.Resource):
    
    @cross_origin()
    def get(self, xosversion,global_threshold, threshold, osmax, osmin):
        
        if xosversion not in ['x','xx','xxx']:
            x,xx,xxx = processOsVersion(xosversion)
            if x is None:
                return jsonify({"Error": "Please specify a xOSversion x, xx, xxx, 5, 5.1, 5.1.2"})
            osmax = x
            osmin = x
            print "x %s" % x
        try:
            threshold = float(threshold)
            global_threshold = float(global_threshold)
        except:
            return jsonify({"Error": "Please specify a valid threshold value like 1,1.3,1.0"})
        print "os_version: %s"% xosversion
        roundby = 2
        try:
            roundby = int(roundby)
        except:
            return jsonify({"Error": "Please specify a valid roundBy value like 1,1.3,1.0"})

        result = iosStat.xStats(xosversion,global_threshold,threshold, roundby,osmax,osmin)
        
        if result == None:
            return jsonify({"Error": "No stats found for this os version"})

        return jsonify(**result)

#api.add_resource(TodoSimple, 'apple/<os_version>')
#api.add_resource(AndroidAPI, '/and/<os_version>/<threshold>')
api.add_resource(IosAPI, '/ios/<xosversion>/<global_threshold>/<threshold>/<osmax>/<osmin>')
api.add_resource(xAndroidAPI, '/and/<xosversion>/<global_threshold>/<threshold>/<osmax>/<osmin>')

if __name__ == '__main__':
    app.run(debug=True, port=8080)
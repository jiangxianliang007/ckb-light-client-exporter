#encoding: utf-8

import requests
import prometheus_client
from prometheus_client import Gauge
from prometheus_client.core import CollectorRegistry
from flask import Response, Flask, request, current_app
import os
import sys


Light_Client_RPC = sys.argv[1]

NodeFlask = Flask(__name__)

def convert_int(value):
    try:
        return int(value)
    except ValueError:
        return int(value, base=16)
    except Exception as exp:
        raise exp

class RpcGet(object):
    def __init__(self, Light_Client_RPC):
        self.Light_Client_RPC = Light_Client_RPC

    def get_light_client_info(self):
        headers = {"Content-Type":"application/json"}
        data = '{"id":1, "jsonrpc":"2.0", "method":"get_tip_header", "params":[]}'
        try:
            r = requests.post(
                url="%s" %(self.Light_Client_RPC),
                data=data,
                headers=headers
            )
            replay = r.json()["result"]
            return {
                "last_blocknumber": convert_int(replay["number"]),
            }
        except:
            return {
                "last_blocknumber": "-1",
            }

@NodeFlask.route("/metrics/lightclient")
def rpc_get():
    CKB_Chain = CollectorRegistry(auto_describe=False)
    Get_Light_Client_Info = Gauge("Get_Light_client_LastBlockInfo",
                                   "Get LastBlockInfo, Show Light client latest block height",
                                   ["light_client_rpc"],
                                   registry=CKB_Chain)

    get_result = RpcGet(Light_Client_RPC)
    light_client_last_block_info = get_result.get_light_client_info()
    Get_Light_Client_Info.labels(
        light_client_rpc=Light_Client_RPC
    ).set(light_client_last_block_info["last_blocknumber"])
    return Response(prometheus_client.generate_latest(CKB_Chain), mimetype="text/plain")

if __name__ == "__main__":
    NodeFlask.run(host="0.0.0.0",port=3000)
    

# ckb-light-client-exporter

docker run -d -it -p 3000:3000 -e light_client_rpc=http://light-client-testnet.ckbapp.dev jiangxianliang/light-client-exporter:20240102

curl http://127.0.0.1:3000/metrics/lightclient


# Clean Network

Clean Network is currently a blockchain network that provides cryptocurrency, NFTs, and other functionalities to support the organizational needs of Inframas.

## How to run Node ( Docker )
docker build -t inframas/cleanetwork-node:local .

docker run --name cleanetwork-node -p 80:80 -d inframas/cleanetwork-node:local
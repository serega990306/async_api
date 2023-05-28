# Async Api
## Python FastAPI web application
### Installation
Before requirements installation install rustup:
```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup install nightly
rustup default nightly
sudo apt install gcc-multilib
```
Start Redis:
```
docker run --name redis -p 6379:6379 -d redis
```
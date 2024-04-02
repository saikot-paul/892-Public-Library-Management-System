### Once you have cloned the repo from github, to run the books and users services:
#### Replace <service> with "books/book" or "users/user" as appropriate
1. Change directory into backend
2. Install the requirements for the backend by (assuming a Linux OS, please google for other OS):
    1. Create a virtual environment by executing: python -m venv venv
    2. Start the virtual environment by executing: source .venv/bin/activate
    3. Install requirements by executing: pip install -r requirements.txt
3. Create a folder "db" in backend/<service>/grpc_server
4. Add a file named config.json and paste the config.json found on discord.
5. Run <service> GRPC client and server by running in terminal:
    1. Change directory to backend/<service>/grpc_server
    2. To start the server, execute: python <service>GRPCServer.py
    3. To start the client, execute: uvicorn <service>GRPCClient:app --reload --port <port_number>
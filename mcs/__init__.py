from mcstatus import JavaServer, BedrockServer


def get_status(address):
    try:
        server = JavaServer.lookup(address)
        return server.status().players.online
    except:
        return 0


def get_ping(address):
    try:
        server = JavaServer.lookup(address)
        return server.ping()
    except:
        return 0


def get_online_player(address):
    temp = []
    try:
        server = JavaServer.lookup(address)
        if len(server.status().players.sample) == 0:
            return temp
        return server.status().players.sample
    except:
        return temp
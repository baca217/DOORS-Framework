def command_handler(sentence, info):
    msg = sentence+" is not a known command"
    func = None

    if sentence == "who is jj geeks":
        msg = "no one will ever know"
    return msg, func

def commands():
    comms = [
            ["who is jj geeks"],
        ]

    ident = [
            "cosine",
        ]
    return comms, ident

{
    "input_alphabet": ["0"],
    "tape_alphabet": ["0","1"],
    "states": ["A","B","C","HALT"],
    "blank_symbol": "0",
    "start_state": "A",
    "halt_states": ["HALT"],

    "transitions": {
        "A": {
            "0": ["B", "1", 1],
            "1": ["HALT", "1", 1]
        },
        "B": {
            "0": ["C","0",1],
            "1": ["B","1",1]
        },
        "C": {
            "0": ["C","1",-1],
            "1": ["A","1",-1]
        }
    }
}

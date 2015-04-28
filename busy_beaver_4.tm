{
    "input_alphabet": ["0"],
    "tape_alphabet": ["0","1"],
    "states": ["A","B","C","D","HALT"],
    "blank_symbol": "0",
    "start_state": "A",
    "halt_states": ["HALT"],
    "output_mod": 1,

    "transitions": {
        "A": {
            "0": ["B", "1", 1],
            "1": ["B", "1", -1]
        },
        "B": {
            "0": ["A","1",-1],
            "1": ["C","0",-1]
        },
        "C": {
            "0": ["HALT","1",1],
            "1": ["D","1",-1]
        },
        "D": {
            "0": ["D", "1", 1],
            "1": ["A", "0", 1]
        }
    }
}

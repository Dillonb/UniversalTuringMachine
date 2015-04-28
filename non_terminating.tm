{
    "input_alphabet": ["0"],
    "tape_alphabet": ["0","1"],
    "states": ["q0","q1"],
    "blank_symbol": "#",
    "start_state": "q0",
    "halt_states": ["q6"],
    "output_mod": 1,
    "input": true,

    "transitions": {
        "q0": {
            "0": ["q0", "1", 1],
            "#": ["q1", "#", -1]
        },
        "q1": {
            "1": ["q1","0",-1],
            "#": ["q0","#",1]
        }
    }
}

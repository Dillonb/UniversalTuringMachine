#!/usr/bin/python3

import json
class UTM:
    dir_left = -1
    dir_right = 1

    # Alphabet: a list containing all valid symbols
    # States: a list of states
    # A list of transitions as defined below
    def __init__(self, alphabet=None, states=None, transitions=None, filename=None):
        if filename is not None:
            f = open(filename)
            data = json.loads(f.read())
            alphabet = data['alphabet']
            states = data['states']
            transitions = data['transitions']

        self.tape = {}
        self.alphabet = alphabet
        self.states = states
        self.transitions = transitions

        self.state = 'q0'
        self.index = 0

    def clean_tape(self):
        """Removes all nulls from either end of the tape."""

        # From beginning
        for key in sorted(self.tape.keys()):
            if self.tape[key] == "null" or self.tape[key] == None:
                if key < self.index:
                    self.tape.pop(key,None)
            else:
                # Stop once we hit a non-null entry.
                break

        # From end
        for key in reversed(sorted(self.tape.keys())):
            if self.tape[key] == "null" or self.tape[key] == None:
                if key > (self.index):
                    self.tape.pop(key,None)
            else:
                # Stop once we hit a non-null entry
                break

    def print_id(self,showIndexes=False):
        if showIndexes:
            print("Index: %i"%(self.index))
        hitNotNull = False
        printedState = False


        if len(self.tape.keys()) > 0:
            minHeadPos = self.index if self.index < min(self.tape.keys()) else min(self.tape.keys())
            maxHeadPos = self.index if self.index > max(self.tape.keys()) else max(self.tape.keys())
        else:
            minHeadPos = self.index
            maxHeadPos = self.index

        for key in range(minHeadPos,maxHeadPos+1):
            if key == self.index:
                print("%s"%(self.state),end=" ")
            if not key in self.tape:
                if key != maxHeadPos:
                    print("null",end=" ")
            else:
                print("%s"%(self.tape[key]),end=" ")
        print("")

    # Instr: a list of input characters
    def processInput(self, inputstring):
        i = 0
        for symbol in inputstring:
            self.tape[i] = symbol
            i += 1

        i = None

        while True:
            # Print the instantaneous description of the TM
            self.clean_tape()
            self.print_id()
            #print(self.tape)
            #self.print_id(True)

            try:
                cur_char = str(self.tape[self.index])
                if cur_char == None:
                    cur_char = "null"
            except KeyError:
                cur_char = "null"

            cur_transition = self.transitions[self.state][cur_char]

            # Write the new symbol
            self.tape[self.index] = cur_transition[1]

            # Should we halt?
            if cur_transition[0] == "HALT":
                break

            # Move along the tape in the correct direction
            self.index += cur_transition[2]

            # Move to the new state
            self.state = cur_transition[0]

        self.clean_tape()
        self.print_id()

tm = UTM(filename="m_modus_n.tm")

tm.processInput(['0','0','0','1','0','0'])

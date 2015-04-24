#!/usr/bin/python3
import json
import os

class UTM:
    dir_left = -1
    dir_right = 1

    # Alphabet: a list containing all valid symbols
    # States: a list of states
    # A list of transitions as defined below
    def __init__(self, input_alphabet=None, tape_alphabet=None, states=None, transitions=None, filename=None, blank_symbol=None, start_state=None):
        if filename is not None:
            f = open(filename)
            data = json.loads(f.read())
            input_alphabet = data['input_alphabet']
            tape_alphabet = data['tape_alphabet']
            states = data['states']
            transitions = data['transitions']
            blank_symbol = data['blank_symbol']
            start_state = data['start_state']
            halt_states = data['halt_states']

        self.tape = {}
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.states = states
        self.transitions = transitions
        self.blank_symbol = blank_symbol
        self.halt_states = halt_states

        self.state = start_state
        self.index = 0

    def clean_tape(self):
        """Removes all nulls from either end of the tape."""

        # From beginning
        for key in sorted(self.tape.keys()):
            if self.tape[key] == self.blank_symbol or self.tape[key] == None:
                if key < self.index:
                    self.tape.pop(key,None)
            else:
                # Stop once we hit a non-null entry.
                break

        # From end
        for key in reversed(sorted(self.tape.keys())):
            if self.tape[key] == self.blank_symbol or self.tape[key] == None:
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
                    print(self.blank_symbol,end=" ")
            else:
                print("%s"%(self.tape[key]),end=" ")
        print("")

    # Instr: a list of input characters
    def processInput(self, inputstring):
        i = 0
        for symbol in inputstring:
            if symbol not in self.input_alphabet:
                print("Invalid input! %s is not in the input alphabet for this TM."%symbol)
                return
            self.tape[i] = symbol
            i += 1

        i = None

        while self.state not in self.halt_states:
            # Print the instantaneous description of the TM
            self.clean_tape()
            self.print_id()
            #print(self.tape)
            #self.print_id(True)

            try:
                cur_char = str(self.tape[self.index])
                if cur_char == None:
                    cur_char = self.blank_symbol
            except KeyError:
                cur_char = self.blank_symbol

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

files = [f for f in os.listdir('.') if os.path.isfile(f) and f[-3:] == ".tm"]

for f in files:
    print("[",files.index(f) + 1, "]", f)

print("Enter the number of the TM you would like to load:")
tmIndex = int(input(">")) - 1
print("Enter an input string")
inputString = list(input(">"))

tm = UTM(filename=files[tmIndex])
tm.processInput(inputString)

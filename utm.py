#!/usr/bin/python3
import json
import os

class Cell:
    previous = None
    next = None
    data = None
    index = None


class Tape:
    start = None
    end = None

    current_head = None

    def get_new_cell(self,value=None):
        c = Cell()
        c.data = value
        return c

    def move_right(self):
        if self.current_head.next is None:
            self.append(None)
        self.current_head = self.current_head.next


    def move_left(self):
        if self.current_head.previous == None:
            self.prepend(None)
        self.current_head = self.current_head.previous

    def get_current_value(self):
        if self.current_head is not None:
            return self.current_head.data
        else:
            return None

    def set_current_value(self,value):
        if self.current_head is not None:
            self.current_head.data = value
        else:
            # First value can be added with append function
            self.append(value)

    def append(self, value=None):
        if self.start == None or self.end == None:
            if self.start != self.end:
                print("ERROR: Only start/only end is set to None. This should never happen.")
            self.start = self.get_new_cell(value)
            self.current_head = self.start
            self.end = self.current_head
            self.start.index = 0
        else:
            self.end.next = self.get_new_cell(value)
            self.end.next.previous = self.end
            self.end = self.end.next
            self.end.index = self.end.previous.index + 1

    def prepend(self, value=None):
        if self.start == None or self.end == None:
            if self.start != self.end:
                print("ERROR: Only start/only end is set to None. This should never happen.")
            self.start = self.get_new_cell(value)
            self.current_head = self.start
            self.end = current_head
            self.start.index = 0
        else:
            self.start.previous = self.get_new_cell(value)
            self.start.previous.next = self.start
            self.start = self.start.previous
            self.start.index = self.start.next.index - 1

    def pop_end(self):
        self.end = self.end.previous
        self.end.next = None

    def pop_start(self):
        self.start = self.start.next
        self.start.previous = None

    def is_empty(self):
        return self.start == None or self.end == None

class UTM:
    dir_left = -1
    dir_right = 1

    # Alphabet: a list containing all valid symbols
    # States: a list of states
    # A list of transitions as defined below
    def __init__(self, input_alphabet=None, tape_alphabet=None, states=None, transitions=None, filename=None, blank_symbol=None, start_state=None,output_mod=1):
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
            output_mod = data['output_mod']

        self.tape = Tape()
        self.input_alphabet = input_alphabet
        self.tape_alphabet = tape_alphabet
        self.states = states
        self.transitions = transitions
        self.blank_symbol = blank_symbol
        self.halt_states = halt_states
        self.output_mod = output_mod

        self.state = start_state

    def clean_tape(self):
        """Removes all nulls from either end of the tape."""

        # Don't need to clean an empty tape.
        if self.tape.start == None or self.tape.end == None:
            return

        # From beginning
        while (self.tape.start.data == None or self.tape.start.data == self.blank_symbol) and self.tape.start.index < self.tape.current_head.index:
            self.tape.pop_start()

        # From end
        while (self.tape.end.data == None or self.tape.end.data == self.blank_symbol) and self.tape.end.index > self.tape.current_head.index:
            self.tape.pop_end()

    def print_id(self,showIndexes=False):
        iterator = self.tape.start

        while iterator is not None:
            if self.tape.current_head.index == iterator.index:
                print("%s"%(self.state), end="")

            print(iterator.data if iterator.data is not None else self.blank_symbol, end="")

            iterator = iterator.next

        print("")

    # Instr: a list of input characters
    def processInput(self, inputstring):
        for symbol in inputstring:
            if symbol not in self.input_alphabet:
                print("Invalid input! %s is not in the input alphabet for this TM."%symbol)
                return
            self.tape.append(symbol)
        steps_taken = 0

        while self.state not in self.halt_states:
            # Print the instantaneous description of the TM, if necessary.
            if not steps_taken % self.output_mod:
                self.clean_tape()
                self.print_id()

            cur_char = self.tape.get_current_value()
            if cur_char == None:
                cur_char = self.blank_symbol

            cur_transition = self.transitions[self.state][cur_char]

            # Write the new symbol
            self.tape.set_current_value(cur_transition[1])

            steps_taken += 1
            if not steps_taken % self.output_mod:
                print("Steps:",steps_taken)
            # Should we halt?
            if cur_transition[0] == "HALT":
                break

            if cur_transition[2] > 0:
                self.tape.move_right()
            else:
                self.tape.move_left()

            # Move to the new state
            self.state = cur_transition[0]

        self.clean_tape()
        self.print_id()
        print("Final total:",steps_taken, "steps.")
files = [f for f in os.listdir('.') if os.path.isfile(f) and f[-3:] == ".tm"]
files = sorted(files)

for f in files:
    print("[",files.index(f) + 1, "]", f)

print("Enter the number of the TM you would like to load:")
tmIndex = int(input(">")) - 1
print("Enter an input string")
inputString = list(input(">"))

tm = UTM(filename=files[tmIndex])
tm.processInput(inputString)

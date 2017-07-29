# Multiplexer-Finder
Produces required multiplexer combination for a given bit pattern
-------------------------------------------------------------------------------
Usage: solver <inputfile> <outputfile>

Program (written in Python) which takes as input a specification of a boolean function, and outputs a minimum sized circuit of 2-to-1 multiplexer gates (MUX) which reproduces this input.

Multiplexer Gate
------------------------
For clarification, here is the logic table for a three input MUX gate used in the resulting circuit the program designs.


|ABC|Out|
|:-----:|:----:|
|000| 0 |
|001| 0 |
|010| 0 |
|011| 1 |
|100| 1 |
|101| 0 |
|110| 1 |
|111| 1 |

Basically, the third input in the mux gate chooses whether to output the first or second input value.  More succinctly

|AB C| Out|
|:----:|:----:|
|Ax 0| A|
|xB 1| B|

A circuit tree of MUX gates, if supplemented with constant 0 and 1 inputs, can produce any boolean function.  In this sense, MUX gates are universal logic gates.


INPUT file specification
------------------------

A 2^N length string of characters {0,1}.

Any boolean function can be represented as a logic table of inputs and outputs, for example here is XOR:

AB| Out|
|:--:|:----:|
|00| 0|
|01| 1|
|10| 1|
|11| 0|

If the inputs are given in "canonical order" any boolean function of N variables can be represented as a 
2^N length string of characters {0,1}. An input file specifying the XOR function would just have the text "0110" saved in it.

Output file specification
-------------------------
A text file with each line specifying a MUX gate

`Q<num>: <input>,<input>,<input>`

Where <num> is the number of this MUX gate (unique).The inputs are given as 0,1 to denote a constant input, or InA,InB,...  where the letters are the function input variables, or Q<num> to specify the output of a previous MUX gate is used as an input here.

Using the XOR function as an example:

Input file:
`0110`

Output file:
`Q0: 1,0,InA`
`Q1: InA,Q0,InB`

There are other solutions with two MUX gates, but at least two gates are 
required so the above output is a minimal sized MUX gate circuit representing 
the XOR function.

Another example, using the AND function:

Input file:
`0001`

Output file:
`Q0: 0,InA,InB`

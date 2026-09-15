module my_sum6 (
    input  wire [5:0] Ain,
    input  wire [5:0] Bin,
    input  wire       Ci,
    output wire [5:0] Sout,
    output wire       Co
);

wire [4:0] c;

full_adder fa0 (
    .a   (Ain[0]),
    .b   (Bin[0]),
    .cin (Ci),
    .sum (Sout[0]),
    .cout(c[0])
);

full_adder fa1 (
    .a   (Ain[1]),
    .b   (Bin[1]),
    .cin (c[0]),
    .sum (Sout[1]),
    .cout(c[1])
);

full_adder fa2 (
    .a   (Ain[2]),
    .b   (Bin[2]),
    .cin (c[1]),
    .sum (Sout[2]),
    .cout(c[2])
);

full_adder fa3 (
    .a   (Ain[3]),
    .b   (Bin[3]),
    .cin (c[2]),
    .sum (Sout[3]),
    .cout(c[3])
);

full_adder fa4 (
    .a   (Ain[4]),
    .b   (Bin[4]),
    .cin (c[3]),
    .sum (Sout[4]),
    .cout(c[4])
);

full_adder fa5 (
    .a   (Ain[5]),
    .b   (Bin[5]),
    .cin (c[4]),
    .sum (Sout[5]),
    .cout(Co)
);

endmodule
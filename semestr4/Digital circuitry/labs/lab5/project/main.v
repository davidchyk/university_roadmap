module decoder_segments (
    input  wire x4,
    input  wire x3,
    input  wire x2,
    input  wire x1,
    output wire a,
    output wire b,
    output wire c,
    output wire d,
    output wire e,
    output wire f,
    output wire g
);

assign a = (x4 | ~x3 | ~x1) &
           (x4 | ~x2) &
           (~x4 | x3 | x2) &
           (~x4 | x1) &
           (x3 | x1) &
           (~x3 | ~x2);

assign b = (x4 | x3) &
           (x4 | x2 | x1) &
           (x4 | ~x2 | ~x1) &
           (~x4 | x2 | ~x1) &
           (x3 | x1);

assign c = (x4 | ~x3) &
           (x4 | ~x1) &
           (~x4 | x3) &
           (x3 | x2) &
           (x2 | ~x1);

assign d = (x4 | x3 | x1) &
           (~x4 | x2) &
           (x3 | ~x2 | ~x1) &
           (~x3 | x2 | ~x1) &
           (~x3 | ~x2 | x1);

assign e = (~x4 | ~x3) &
           (~x4 | ~x2) &
           (x3 | x1) &
           (~x2 | x1);

assign f = (x4 | ~x3 | x2) &
           (~x4 | x3) &
           (~x4 | ~x2) &
           (~x3 | x1) &
           (x2 | x1);

assign g = (~x4 & ~x3 & ~x2) |
           (~x4 & x3 & x2 & x1) |
           (x4 & x3 & ~x2 & ~x1);

endmodule

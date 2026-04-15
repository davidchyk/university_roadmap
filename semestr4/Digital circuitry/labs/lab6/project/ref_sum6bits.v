module ref_sum6 (
    input  wire [5:0] Ain,
    input  wire [5:0] Bin,
    input  wire       Ci,
    output wire [5:0] Sout,
    output wire       Co
);

wire [6:0] temp;

assign temp = Ain + Bin + Ci;
assign Sout = temp[5:0];
assign Co   = temp[6];

endmodule
module test_sum6;

reg  [5:0] Ain_r, Bin_r;
reg        Ci_r;

wire [5:0] Ain, Bin;
wire       Ci;

wire [5:0] res_my, res_ref;
wire       cm, cr;

assign Ain = Ain_r;
assign Bin = Bin_r;
assign Ci  = Ci_r;

my_sum6  my_block  (
    .Ain (Ain),
    .Bin (Bin),
    .Ci  (Ci),
    .Sout(res_my),
    .Co  (cm)
);

ref_sum6 ref_block (
    .Ain (Ain),
    .Bin (Bin),
    .Ci  (Ci),
    .Sout(res_ref),
    .Co  (cr)
);

initial
begin
    $display("Time\tAin\tBin\tCi\tres_my\tcm\tres_ref\tcr");
    $monitor("%0t\t%b\t%b\t%b\t%b\t%b\t%b\t%b",
             $time, Ain, Bin, Ci, res_my, cm, res_ref, cr);
end

initial
begin
    Ain_r = 6'b000000;
    Bin_r = 6'b000000;
    Ci_r  = 1'b0;

    #10 Ain_r = 6'b000001; Bin_r = 6'b000010; Ci_r = 1'b0; // 1 + 2
    #10 Ain_r = 6'b000101; Bin_r = 6'b000011; Ci_r = 1'b0; // 5 + 3
    #10 Ain_r = 6'b001111; Bin_r = 6'b000001; Ci_r = 1'b0; // 15 + 1
    #10 Ain_r = 6'b010101; Bin_r = 6'b001010; Ci_r = 1'b1; // 21 + 10 + 1
    #10 Ain_r = 6'b111111; Bin_r = 6'b000001; Ci_r = 1'b0; // overflow
    #10 Ain_r = 6'b101010; Bin_r = 6'b010101; Ci_r = 1'b1;
    #10 Ain_r = 6'b111100; Bin_r = 6'b000011; Ci_r = 1'b1;
    #10 Ain_r = 6'b100000; Bin_r = 6'b100000; Ci_r = 1'b0;
    #10 Ain_r = 6'b011111; Bin_r = 6'b011111; Ci_r = 1'b1;
    #10 $finish;
end

endmodule
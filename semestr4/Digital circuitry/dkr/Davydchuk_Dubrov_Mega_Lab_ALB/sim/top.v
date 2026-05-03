`timescale 1 ns / 1 ps

module top;
    parameter WIDTH = 12;

    wire [WIDTH-1:0] A_ALB;
    wire [WIDTH-1:0] B_ALB;
    wire [WIDTH-1:0] F_ALB;
    wire [WIDTH-1:0] F_NORM;
    wire [WIDTH-1:0] F_REF;
    wire [WIDTH-1:0] F_NORM_REF;
    wire CI;
    wire [1:0] ALB_MI;
    wire CO;
    wire VO;
    wire NO;
    wire ZO;
    wire NORM_RIGHT;
    wire CO_REF;
    wire VO_REF;
    wire NO_REF;
    wire ZO_REF;
    wire NORM_RIGHT_REF;
    reg clock;
    reg resetb;

    alb #(WIDTH) dut (
        .F_ALB(F_ALB),
        .F_NORM(F_NORM),
        .CO(CO),
        .VO(VO),
        .NO(NO),
        .ZO(ZO),
        .NORM_RIGHT(NORM_RIGHT),
        .A_ALB(A_ALB),
        .B_ALB(B_ALB),
        .CI(CI),
        .ALB_MI(ALB_MI),
        .clock(clock),
        .resetb(resetb)
    );

    alb_ref #(WIDTH) ref_model (
        .F_REF(F_REF),
        .F_NORM_REF(F_NORM_REF),
        .CO_REF(CO_REF),
        .VO_REF(VO_REF),
        .NO_REF(NO_REF),
        .ZO_REF(ZO_REF),
        .NORM_RIGHT_REF(NORM_RIGHT_REF),
        .A_ALB(A_ALB),
        .B_ALB(B_ALB),
        .CI(CI),
        .ALB_MI(ALB_MI),
        .clock(clock),
        .resetb(resetb)
    );

    stimulus #(WIDTH) stim (
        .A_ALB(A_ALB),
        .B_ALB(B_ALB),
        .CI(CI),
        .ALB_MI(ALB_MI),
        .clock(clock),
        .resetb(resetb)
    );

    checker #(WIDTH) check (
        .F_ALB(F_ALB),
        .F_NORM(F_NORM),
        .CO(CO),
        .VO(VO),
        .NO(NO),
        .ZO(ZO),
        .NORM_RIGHT(NORM_RIGHT),
        .F_REF(F_REF),
        .F_NORM_REF(F_NORM_REF),
        .CO_REF(CO_REF),
        .VO_REF(VO_REF),
        .NO_REF(NO_REF),
        .ZO_REF(ZO_REF),
        .NORM_RIGHT_REF(NORM_RIGHT_REF),
        .clock(clock),
        .resetb(resetb)
    );

    initial begin
        clock = 1'b0;
        forever #5 clock = ~clock;
    end

    initial begin
        resetb = 1'b0;
        #20 resetb = 1'b1;
    end
endmodule

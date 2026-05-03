`timescale 1 ns / 1 ps

module checker
#(
    parameter WIDTH = 12
)
(
    input [WIDTH-1:0] F_ALB,
    input [WIDTH-1:0] F_NORM,
    input CO,
    input VO,
    input NO,
    input ZO,
    input NORM_RIGHT,
    input [WIDTH-1:0] F_REF,
    input [WIDTH-1:0] F_NORM_REF,
    input CO_REF,
    input VO_REF,
    input NO_REF,
    input ZO_REF,
    input NORM_RIGHT_REF,
    input clock,
    input resetb
);
    integer errors;

    initial begin
        errors = 0;
    end

    always @(negedge clock) begin
        if (resetb == 1'b1) begin
            if ({CO, VO, NO, ZO, NORM_RIGHT, F_ALB, F_NORM} ==
                {CO_REF, VO_REF, NO_REF, ZO_REF, NORM_RIGHT_REF, F_REF, F_NORM_REF}) begin
                $display("%0t correct F=%b FN=%b C=%b V=%b N=%b Z=%b NR=%b",
                         $time, F_ALB, F_NORM, CO, VO, NO, ZO, NORM_RIGHT);
            end else begin
                errors = errors + 1;
                $display("%0t error dut=%b_%b_%b_%b_%b_%b_%b ref=%b_%b_%b_%b_%b_%b_%b",
                         $time, CO, VO, NO, ZO, NORM_RIGHT, F_ALB, F_NORM,
                         CO_REF, VO_REF, NO_REF, ZO_REF, NORM_RIGHT_REF,
                         F_REF, F_NORM_REF);
            end
        end
    end

    initial begin
        #220;
        if (errors == 0) begin
            $display("TEST PASSED");
        end else begin
            $display("TEST FAILED: %0d errors", errors);
        end
    end
endmodule

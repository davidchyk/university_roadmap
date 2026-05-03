`timescale 1 ns / 1 ps

module stimulus
#(
    parameter WIDTH = 12
)
(
    output reg [WIDTH-1:0] A_ALB,
    output reg [WIDTH-1:0] B_ALB,
    output reg CI,
    output reg [1:0] ALB_MI,
    input clock,
    input resetb
);
    task apply_vector;
        input [1:0] mi;
        input [WIDTH-1:0] a;
        input [WIDTH-1:0] b;
        input ci;
        begin
            @(negedge clock);
            ALB_MI = mi;
            A_ALB = a;
            B_ALB = b;
            CI = ci;
        end
    endtask

    initial begin
        A_ALB = {WIDTH{1'b0}};
        B_ALB = {WIDTH{1'b0}};
        CI = 1'b0;
        ALB_MI = 2'b00;

        wait (resetb == 1'b0);
        wait (resetb == 1'b1);

        apply_vector(2'b00, 12'b000000001010, 12'b000000000101, 1'b0);
        apply_vector(2'b11, 12'b000000001010, 12'b000000000101, 1'b1);

        apply_vector(2'b01, 12'b000000000001, 12'b000000000001, 1'b0);
        apply_vector(2'b01, 12'b000000000000, 12'b000000000000, 1'b0);
        apply_vector(2'b01, 12'b0110001110, 12'b1010010111, 1'b0);
        apply_vector(2'b01, 12'b000110001110, 12'b001010010111, 1'b0);
        apply_vector(2'b01, 12'b1101101000, 12'b111001110001, 1'b1);
        apply_vector(2'b01, 12'b011000000000, 12'b001100000000, 1'b0);
        apply_vector(2'b01, 12'b100100000000, 12'b101000000000, 1'b0);

        apply_vector(2'b10, 12'b000000000001, 12'b000000000011, 1'b1);
        apply_vector(2'b10, 12'b000000000011, 12'b000000000001, 1'b1);
        apply_vector(2'b10, 12'b001010010111, 12'b000110001110, 1'b1);
        apply_vector(2'b10, 12'b000110001110, 12'b110101101001, 1'b1);

        apply_vector(2'b01, 12'b111111111111, 12'b000000000001, 1'b0);
        apply_vector(2'b00, 12'b101010101010, 12'b010101010101, 1'b0);

        repeat (8) @(posedge clock);
        $finish;
    end
endmodule

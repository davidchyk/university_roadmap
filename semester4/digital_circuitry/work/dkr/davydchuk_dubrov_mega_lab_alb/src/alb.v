`timescale 1 ns / 1 ps

module alb
#(
    parameter WIDTH = 12
)
(
    output reg [WIDTH-1:0] F_ALB,
    output reg [WIDTH-1:0] F_NORM,
    output reg CO,
    output reg VO,
    output reg NO,
    output reg ZO,
    output reg NORM_RIGHT,
    input [WIDTH-1:0] A_ALB,
    input [WIDTH-1:0] B_ALB,
    input CI,
    input [1:0] ALB_MI,
    input clock,
    input resetb
);
    reg [WIDTH-1:0] RgA;
    reg [WIDTH-1:0] RgB;
    reg RgCI;
    reg [1:0] RgMI;

    reg [WIDTH:0] ext_result;
    reg [WIDTH-1:0] raw_result;
    reg carry_result;
    reg overflow_result;

    always @(posedge clock or negedge resetb) begin
        if (resetb == 1'b0) begin
            RgA <= {WIDTH{1'b0}};
            RgB <= {WIDTH{1'b0}};
            RgCI <= 1'b0;
            RgMI <= 2'b00;
        end else begin
            RgA <= A_ALB;
            RgB <= B_ALB;
            RgCI <= CI;
            RgMI <= ALB_MI;
        end
    end

    always @(*) begin
        ext_result = {1'b0, RgA | RgB};
        raw_result = RgA | RgB;
        carry_result = 1'b0;
        overflow_result = 1'b0;

        case (RgMI)
            2'b00: begin
                ext_result = {1'b0, RgA | RgB};
                raw_result = ext_result[WIDTH-1:0];
            end
            2'b01: begin
                ext_result = {1'b0, RgA} + {1'b0, RgB} + RgCI;
                raw_result = ext_result[WIDTH-1:0];
                carry_result = ext_result[WIDTH];
                overflow_result = (RgA[WIDTH-1] == RgB[WIDTH-1]) &&
                                  (raw_result[WIDTH-1] != RgA[WIDTH-1]);
            end
            2'b10: begin
                ext_result = {1'b0, RgB} + {1'b0, ~RgA} + RgCI;
                raw_result = ext_result[WIDTH-1:0];
                carry_result = ext_result[WIDTH];
                overflow_result = (RgB[WIDTH-1] != RgA[WIDTH-1]) &&
                                  (raw_result[WIDTH-1] != RgB[WIDTH-1]);
            end
            2'b11: begin
                ext_result = {1'b0, RgA | RgB};
                raw_result = ext_result[WIDTH-1:0];
            end
        endcase
    end

    always @(*) begin
        F_ALB = raw_result;
        CO = carry_result;
        VO = overflow_result;
        NO = raw_result[WIDTH-1];
        ZO = (raw_result == {WIDTH{1'b0}});

        NORM_RIGHT = overflow_result && (raw_result[WIDTH-1] != raw_result[WIDTH-2]);
        if (NORM_RIGHT) begin
            F_NORM = {raw_result[WIDTH-1], raw_result[WIDTH-1:1]};
        end else begin
            F_NORM = raw_result;
        end
    end
endmodule

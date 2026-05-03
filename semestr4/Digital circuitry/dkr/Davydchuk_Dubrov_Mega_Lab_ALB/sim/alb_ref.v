`timescale 1 ns / 1 ps

module alb_ref
#(
    parameter WIDTH = 12
)
(
    output reg [WIDTH-1:0] F_REF,
    output reg [WIDTH-1:0] F_NORM_REF,
    output reg CO_REF,
    output reg VO_REF,
    output reg NO_REF,
    output reg ZO_REF,
    output reg NORM_RIGHT_REF,
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
    reg [WIDTH:0] temp;

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
        temp = {1'b0, RgA | RgB};
        CO_REF = 1'b0;
        VO_REF = 1'b0;

        case (RgMI)
            2'b00: temp = {1'b0, RgA | RgB};
            2'b01: begin
                temp = {1'b0, RgA} + {1'b0, RgB} + RgCI;
                CO_REF = temp[WIDTH];
                VO_REF = (RgA[WIDTH-1] == RgB[WIDTH-1]) &&
                         (temp[WIDTH-1] != RgA[WIDTH-1]);
            end
            2'b10: begin
                temp = {1'b0, RgB} + {1'b0, ~RgA} + RgCI;
                CO_REF = temp[WIDTH];
                VO_REF = (RgB[WIDTH-1] != RgA[WIDTH-1]) &&
                         (temp[WIDTH-1] != RgB[WIDTH-1]);
            end
            2'b11: temp = {1'b0, RgA | RgB};
        endcase

        F_REF = temp[WIDTH-1:0];
        NO_REF = F_REF[WIDTH-1];
        ZO_REF = (F_REF == {WIDTH{1'b0}});
        NORM_RIGHT_REF = VO_REF && (F_REF[WIDTH-1] != F_REF[WIDTH-2]);

        if (NORM_RIGHT_REF) begin
            F_NORM_REF = {F_REF[WIDTH-1], F_REF[WIDTH-1:1]};
        end else begin
            F_NORM_REF = F_REF;
        end
    end
endmodule

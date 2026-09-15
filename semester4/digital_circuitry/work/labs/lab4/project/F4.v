module F4(x1, x2, x3, f);
  input x1, x2, x3;
  output f;
  assign f = ~(~(x2 & x1) & ~(x3 & x1));
endmodule
module design_v1 (
    input signed [7:0] X,
    output [7:0] abs_result
);

    // Combinational: full comparison and conditional negation
    assign abs_result = (X < 0) ? (-X) : X;

endmodule
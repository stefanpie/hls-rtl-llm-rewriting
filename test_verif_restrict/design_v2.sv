module design_v2 (
    input signed [7:0] X,
    output [7:0] abs_result
);

    // Combinational: just pass through (X guaranteed non-negative)
    assign abs_result = X;

endmodule
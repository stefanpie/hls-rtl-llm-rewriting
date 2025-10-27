module equiv_check (
    input signed [7:0] X,
    output [7:0] out1,
    output [7:0] out2
);

    design_v1 dut1 (.X(X), .abs_result(out1));
    design_v2 dut2 (.X(X), .abs_result(out2));

    // CONSTRAINT: X is always non-negative
    assume property ((X >= 0));

    // EQUIVALENCE
    assert property ((out1 == out2));

    // DEBUG COVERS
    cover property ((X == 0));
    cover property ((X > 0));
    cover property ((X == 127));
endmodule
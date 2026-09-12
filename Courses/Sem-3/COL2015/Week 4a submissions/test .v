`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/11/2026 02:12:46 PM
// Design Name: 
// Module Name: test
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////


`timescale 1ns/1ps

module tb_lab4a;

    reg [7:0] A,B;
    reg [3:0] threshold;

    wire [7:0] difference;
    wire [3:0] distance;
    wire equal,within_threshold;

    integer i,j,t;
    integer expected_difference,expected_distance;
    integer expected_equal,expected_within;
    integer errors,total_tests;

    hamming_distance8 dut(
        A,B,threshold,
        difference,distance,equal,within_threshold
    );

    function integer calc_distance;
        input [7:0] x;
        begin
            calc_distance=x[0]+x[1]+x[2]+x[3]+x[4]+x[5]+x[6]+x[7];
        end
    endfunction

    initial begin

        errors=0;
        total_tests=0;

        for(t=0;t<16;t=t+1) begin
            threshold=t;

            for(i=0;i<256;i=i+1) begin
                A=i;

                for(j=0;j<256;j=j+1) begin
                    B=j;
                    #1;

                    expected_difference=i^j;
                    expected_distance=calc_distance(i^j);
                    expected_equal=(i==j);
                    expected_within=(expected_distance<=t);

                    total_tests=total_tests+1;

                    if(difference!==expected_difference) begin
                        $display("ERROR: A=%b B=%b T=%d difference=%b expected=%b",
                                 A,B,threshold,difference,expected_difference);
                        errors=errors+1;
                    end

                    if(distance!==expected_distance) begin
                        $display("ERROR: A=%b B=%b T=%d distance=%d expected=%d",
                                 A,B,threshold,distance,expected_distance);
                        errors=errors+1;
                    end

                    if(equal!==expected_equal) begin
                        $display("ERROR: A=%b B=%b equal=%b expected=%b",
                                 A,B,equal,expected_equal);
                        errors=errors+1;
                    end

                    if(within_threshold!==expected_within) begin
                        $display("ERROR: A=%b B=%b T=%d within=%b expected=%b",
                                 A,B,threshold,within_threshold,expected_within);
                        errors=errors+1;
                    end
                end
            end

            $display("Threshold %d done",t);
        end

        $display("\n==============================");
        $display("Total tests  = %d",total_tests);
        $display("Total errors = %d",errors);

        if(errors==0)
            $display("PASS: ALL TESTS PASSED!");
        else
            $display("FAIL: ERRORS DETECTED!");

        $display("==============================");

        $finish;
    end

endmodule

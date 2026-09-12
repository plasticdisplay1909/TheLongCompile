`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 09/11/2026 02:11:45 PM
// Design Name: 
// Module Name: code
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


module full_adder(
    input wire a,b,cin,
    output wire sum,cout
);
    assign sum=a^b^cin;
    assign cout=(a&b)|(a&cin)|(b&cin);
endmodule


module popcount8(
    input wire [7:0] x,
    output wire [3:0] count
);

    wire [1:0] p0,p1,p2,p3;
    wire [2:0] s0,s1;
    wire c01,c23,c0,c1;

    full_adder f0(x[0],x[1],1'b0,p0[0],p0[1]);
    full_adder f1(x[2],x[3],1'b0,p1[0],p1[1]);
    full_adder f2(x[4],x[5],1'b0,p2[0],p2[1]);
    full_adder f3(x[6],x[7],1'b0,p3[0],p3[1]);

    full_adder f4(p0[0],p1[0],1'b0,s0[0],c01);
    full_adder f5(p0[1],p1[1],c01,s0[1],s0[2]);

    full_adder f6(p2[0],p3[0],1'b0,s1[0],c23);
    full_adder f7(p2[1],p3[1],c23,s1[1],s1[2]);

    full_adder f8(s0[0],s1[0],1'b0,count[0],c0);
    full_adder f9(s0[1],s1[1],c0,count[1],c1);
    full_adder f10(s0[2],s1[2],c1,count[2],count[3]);

endmodule


module comparator4(
    input wire [3:0] a,b,
    output wire a_le_b
);

    wire e3,e2,e1,e0;
    wire greater;

    assign e3=~(a[3]^b[3]);
    assign e2=~(a[2]^b[2]);
    assign e1=~(a[1]^b[1]);
    assign e0=~(a[0]^b[0]);

    assign greater=(a[3]&~b[3])|
                   (e3&a[2]&~b[2])|
                   (e3&e2&a[1]&~b[1])|
                   (e3&e2&e1&a[0]&~b[0]);

    assign a_le_b=~greater;

endmodule


module comparator8(
    input wire [7:0] a,b,
    output wire equal
);

    wire [7:0] diff;

    assign diff=a^b;
    assign equal=~(|diff);

endmodule


module hamming_distance8(
    input wire [7:0] A,
    input wire [7:0] B,
    input wire [3:0] threshold,
    output wire [7:0] difference,
    output wire [3:0] distance,
    output wire equal,
    output wire within_threshold
);

    assign difference=A^B;

    popcount8 pc(difference,distance);
    comparator8 eq(A,B,equal);
    comparator4 cmp(distance,threshold,within_threshold);

endmodule

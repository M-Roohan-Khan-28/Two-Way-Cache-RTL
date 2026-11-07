`timescale 1ns/1ps
// Independent two-way array oracle. No DUT storage or DUT result feeds expected values.
module cache_contract_test;
  logic clk=0, reset=0, write=0, way_select=0;
  logic [2:0] tag=0;
  logic [1:0] index=0;
  logic [7:0] data_in=0;
  wire [7:0] data_out;
  wire hit;
  cache_2way dut(.*);
  always #5 clk=~clk;

  bit ref_valid[0:1][0:3];
  logic [2:0] ref_tag[0:1][0:3];
  logic [7:0] ref_data[0:1][0:3];
  int checks=0, writes=0, resets=0;
  int unsigned rng=32'h28cace17;

  function automatic logic [7:0] next_byte();
    rng ^= rng << 13;
    rng ^= rng >> 17;
    rng ^= rng << 5;
    return rng[7:0];
  endfunction

  task automatic clear_reference;
    for(int w=0;w<2;w++)
      for(int s=0;s<4;s++) begin
        ref_valid[w][s]=0;
        ref_tag[w][s]=0;
        ref_data[w][s]=0;
      end
  endtask

  task automatic check_lookup(input int s,input int t,input string label);
    bit expected_hit;
    logic [7:0] expected_data;
    write=0;
    index=s[1:0]; tag=t[2:0];
    expected_hit=0; expected_data=0;
    if(ref_valid[0][s] && ref_tag[0][s] == t[2:0]) begin
      expected_hit=1; expected_data=ref_data[0][s];
    end else if(ref_valid[1][s] && ref_tag[1][s] == t[2:0]) begin
      expected_hit=1; expected_data=ref_data[1][s];
    end
    #1;
    if(hit !== expected_hit || data_out !== expected_data)
      $fatal(1,"CACHE_MISMATCH %s set=%0d tag=%0d expected_hit=%b observed_hit=%b expected_data=%02h observed_data=%02h",
             label,s,t,expected_hit,hit,expected_data,data_out);
    checks++;
  endtask

  task automatic query_all(input string label);
    for(int s=0;s<4;s++)
      for(int t=0;t<8;t++) check_lookup(s,t,label);
  endtask

  task automatic put(input int w,input int s,input int t,input logic [7:0] value);
    @(negedge clk);
    way_select=w[0]; index=s[1:0]; tag=t[2:0]; data_in=value; write=1;
    @(posedge clk);
    ref_valid[w][s]=1; ref_tag[w][s]=t[2:0]; ref_data[w][s]=value;
    #1; write=0;
    check_lookup(s,t,"post-write");
    writes++;
  endtask

  task automatic pulse_reset(input string label);
    @(negedge clk);
    #2; reset=1;
    clear_reference(); resets++;
    #1; query_all(label);
    @(negedge clk); reset=0;
    query_all("post-reset");
  endtask

  initial begin
    clear_reference();
    reset=1;
    repeat(2) @(posedge clk);
    #1; query_all("initial reset");
    @(negedge clk); reset=0;
    query_all("empty");

    // Every way, set, and tag; each write has a seeded independent byte.
    for(int w=0;w<2;w++)
      for(int s=0;s<4;s++)
        for(int t=0;t<8;t++) begin
          put(w,s,t,next_byte());
          for(int q=0;q<8;q++) check_lookup(s,q,"tag sweep");
        end
    query_all("all sets filled");

    // Exhaust all possible byte payloads at one way/set/tag.
    for(int value=0;value<256;value++) begin
      put(0,0,0,value[7:0]);
      check_lookup(0,0,"byte sweep");
      check_lookup(0,7,"unselected tag isolation");
    end

    // Duplicate tag must prefer way 0; replacing it exposes way 1.
    put(0,3,5,8'hA5);
    put(1,3,5,8'h3C);
    check_lookup(3,5,"duplicate way-zero priority");
    put(0,3,4,8'h72);
    check_lookup(3,5,"way-one after way-zero replacement");
    check_lookup(3,4,"way-zero replacement");

    repeat(3) @(posedge clk);
    query_all("no-write preservation");
    pulse_reset("asynchronous reset after population");

    // A write while reset is asserted must not take effect.
    @(negedge clk); reset=1; write=1; way_select=1; index=3; tag=7; data_in=8'hF0;
    clear_reference(); resets++;
    repeat(2) @(posedge clk);
    #1; write=0; query_all("reset/write priority");
    @(negedge clk); reset=0;
    query_all("reset release");
    put(1,3,7,8'h4E);
    query_all("post-reset refill");

    $display("CACHE_CONTRACT_PASS checks=%0d writes=%0d resets=%0d seed=0x28CACE17",checks,writes,resets);
    $finish;
  end
  initial begin #200000; $fatal(1,"CACHE_TIMEOUT bounded test did not finish"); end
endmodule

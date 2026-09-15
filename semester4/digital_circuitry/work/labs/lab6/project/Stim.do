vlib work

vlog full_adder.v
vlog sum6bits.v
vlog ref_sum6bits.v
vlog test.v

vsim work.test_sum6

add wave sim:/test_sum6/Ain
add wave sim:/test_sum6/Bin
add wave sim:/test_sum6/Ci
add wave sim:/test_sum6/res_my
add wave sim:/test_sum6/cm
add wave sim:/test_sum6/res_ref
add wave sim:/test_sum6/cr

run -all
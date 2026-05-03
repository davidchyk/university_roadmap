transcript on
if {[file exists work/_info]} {
    echo "Reusing existing work library"
} elseif {[file exists work]} {
    echo "Using existing work directory"
} else {
    vlib work
}
vlog ../src/alb.v alb_ref.v stimulus.v checker.v top.v
vsim work.top
add wave -radix binary sim:/top/clock
add wave -radix binary sim:/top/resetb
add wave -radix binary sim:/top/ALB_MI
add wave -radix binary sim:/top/CI
add wave -radix binary sim:/top/A_ALB
add wave -radix binary sim:/top/B_ALB
add wave -radix binary sim:/top/F_ALB
add wave -radix binary sim:/top/F_NORM
add wave -radix binary sim:/top/CO
add wave -radix binary sim:/top/VO
add wave -radix binary sim:/top/NO
add wave -radix binary sim:/top/ZO
add wave -radix binary sim:/top/NORM_RIGHT
run -all

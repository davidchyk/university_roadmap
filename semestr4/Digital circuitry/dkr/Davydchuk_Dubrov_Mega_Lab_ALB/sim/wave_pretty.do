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

delete wave *

add wave -divider "Clock and reset"
add wave -radix binary sim:/top/clock
add wave -radix binary sim:/top/resetb

add wave -divider "Control"
add wave -radix binary sim:/top/ALB_MI
add wave -radix binary sim:/top/CI

add wave -divider "Operands"
add wave -radix binary sim:/top/A_ALB
add wave -radix binary sim:/top/B_ALB

add wave -divider "ALB result"
add wave -radix binary sim:/top/F_ALB
add wave -radix binary sim:/top/F_NORM

add wave -divider "Reference result"
add wave -radix binary sim:/top/F_REF
add wave -radix binary sim:/top/F_NORM_REF

add wave -divider "Flags"
add wave -radix binary sim:/top/CO
add wave -radix binary sim:/top/VO
add wave -radix binary sim:/top/NO
add wave -radix binary sim:/top/ZO
add wave -radix binary sim:/top/NORM_RIGHT

add wave -divider "Reference flags"
add wave -radix binary sim:/top/CO_REF
add wave -radix binary sim:/top/VO_REF
add wave -radix binary sim:/top/NO_REF
add wave -radix binary sim:/top/ZO_REF
add wave -radix binary sim:/top/NORM_RIGHT_REF

configure wave -namecolwidth 180
configure wave -valuecolwidth 120
configure wave -justifyvalue left
configure wave -signalnamewidth 1
configure wave -timelineunits ns
configure wave -gridoffset 0
configure wave -gridperiod 10
configure wave -griddelta 40

run -all
wave zoom full

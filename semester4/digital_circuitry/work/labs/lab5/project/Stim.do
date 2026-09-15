vlib work
vlog main.v
vsim work.decoder_segments

add wave x4
add wave x3
add wave x2
add wave x1
add wave a
add wave b
add wave c
add wave d
add wave e
add wave f
add wave g

force x4 0 0ns, 1 80ns
force x3 0 0ns, 1 40ns, 0 80ns, 1 120ns
force x2 0 0ns, 1 20ns, 0 40ns, 1 60ns, 0 80ns, 1 100ns, 0 120ns, 1 140ns
force x1 0 0ns, 1 10ns, 0 20ns, 1 30ns, 0 40ns, 1 50ns, 0 60ns, 1 70ns, \
         0 80ns, 1 90ns, 0 100ns, 1 110ns, 0 120ns, 1 130ns, 0 140ns, 1 150ns

run 160ns
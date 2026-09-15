onerror {exit -code 1}
vlib work
vlog -work work DavydchukArtem_IO41_lab1.vo
vlog -work work Waveform.vwf.vt
vsim -novopt -c -t 1ps -L cycloneiii_ver -L altera_ver -L altera_mf_ver -L 220model_ver -L sgate work.DavydchukArtem_IO41_lab1_vlg_vec_tst -voptargs="+acc"
vcd file -direction DavydchukArtem_IO41_lab1.msim.vcd
vcd add -internal DavydchukArtem_IO41_lab1_vlg_vec_tst/*
vcd add -internal DavydchukArtem_IO41_lab1_vlg_vec_tst/i1/*
run -all
quit -f

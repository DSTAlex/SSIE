onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate -format Logic /tb_myfour/stopop
add wave -noupdate -format Logic /tb_myfour/doorsensor
add wave -noupdate -format Logic /tb_myfour/stopplate
add wave -noupdate -format Literal /tb_myfour/timing
add wave -noupdate -format Literal -radix unsigned /tb_myfour/duration
add wave -noupdate -format Literal -radix unsigned /tb_myfour/dut/timer
add wave -noupdate -format Literal /tb_myfour/heatsetting
add wave -noupdate -format Literal /tb_myfour/dut/state
add wave -noupdate -format Literal -expand /tb_myfour/start_vec
add wave -noupdate -format Logic /tb_myfour/plate_engine
add wave -noupdate -format Logic /tb_myfour/ring
add wave -noupdate -format Logic /tb_myfour/g_engine
add wave -noupdate -format Logic /tb_myfour/mw_engine
add wave -noupdate -format Literal /tb_myfour/timedisplay
add wave -noupdate -format Literal /tb_myfour/thermostat
add wave -noupdate -format Literal /tb_myfour/microwavepower
add wave -noupdate -format Logic /tb_myfour/nreset
add wave -noupdate -format Logic /tb_myfour/clock
add wave -noupdate -format Literal /tb_myfour/start
add wave -noupdate -format Literal /tb_myfour/heat
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {105032 ns}
WaveRestoreZoom {104949 ns} {105018 ns}
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0

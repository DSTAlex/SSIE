# Changer de répertoire dans MODELSIM
vlib work

vcom -93 MyFour.vhd       
vcom -93 tb_MyFour.vhd

vsim tb_MyFour

view wave
view structure
view signals

add wave *

run -a
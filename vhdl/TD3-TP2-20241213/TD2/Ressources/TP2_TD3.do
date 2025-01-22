# Changer de répertoire dans MODELSIM
vlib work

vcom -93 MyFour.vhd       
vcom -93 tb_MyFour_notext.vhd

vsim tb_MyFour

view wave
view structure
view signals

#add wave *
do wave.do

run -a
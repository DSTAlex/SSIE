# Changer de répertoire dans MODELSIM
vlib work
vmap TD1_Exo3 work


vcom -93 MUX_BUS_4to1.vhd       
vcom -93 tb_MUX.vhd

vsim cf_u0RTL1_u1RTL2

view wave
view structure
view signals

add wave *

run -a
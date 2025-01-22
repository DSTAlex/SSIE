library ieee;
use ieee.std_logic_1164.all;
use IEEE.math_real.all;


entity my_entity3 is
    port (
        max : in integer;
        compter_precharge: in integer;
        increase : in BOOLEAN; -- true for increase ; flase for decrease
        Reset : in BOOLEAN;
        Clk : in std_logic
    );
end my_entity3;

architecture td1_exo4 of my_entity3 is
     
    signal my_output : integer;

begin
    compter : process(Reset) 
    variable sens: integer;
    begin
        if (Reset) then
            my_output<= compter_precharge;
        end if;

        if (increase) then
            sens := 1;
        else
            sens := -1;
        end if;

        if (Clk'event and Clk='1') then
            my_output <= my_output + sens;
            if (my_output=max and increase) then
                my_output <= 0;
            else
                if(my_output=-1 and not increase) then
                    my_output <= max - 1;
                end if;
            end if;
        end if;
    end process compter;



end td1_exo4;

 
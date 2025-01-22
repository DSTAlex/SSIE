library ieee;
use ieee.std_logic_1164.all;
use IEEE.math_real.all;


entity my_entity2 is
    port (
        input0 : in STD_LOGIC_VECTOR;
        input1 : in STD_LOGIC_VECTOR;
        input2 : in STD_LOGIC_VECTOR;
        input3 : in STD_LOGIC_VECTOR;
        choose : in STD_LOGIC_VECTOR -- encode in 2 bit
    );
end my_entity2;

architecture td1_exo3 of my_entity2 is
     
    signal my_output : STD_LOGIC_VECTOR;

begin
    multiplexing_Q1 : process(my_output, input1, input2, input3, input0, choose)
    begin
        if choose(1) = '1' then
            if choose(0) = '1' then
                my_output <= input3;
            else
                my_output <= input2;
            end if;
        else
            if choose(0) = '1' then
                my_output <= input1;
            else
                my_output <= input0;
            end if;
        end if;
    end process multiplexing_Q1;

    multiplexing_Q2 : process(my_output, input0, input1, input2, input3)
        variable choosed : integer;
    begin
        choosed := 0;
        for i in choose'range loop
            if choose(i) = '1' then
                choosed := choosed + i ** 2;
            end if;
        end loop;
        case choosed is
            when 0 => my_output <= input0;
            when 1 => my_output <= input1;
            when 2 => my_output <= input2;
            when 3 => my_output <= input3;
        end case;
    end process multiplexing_Q2;

end td1_exo3;

 
library ieee;
use ieee.std_logic_1164.all;
use IEEE.math_real.all;


entity my_entity is
    port (
        integer_input : in INTEGER;
        vector_input : in STD_LOGIC_VECTOR
    );
end my_entity;

architecture td1_exo2 of my_entity is
 
    signal vector_out : STD_LOGIC_VECTOR;
    signal integer_out : INTEGER   := 0;
     
begin
    vector_to_int : process(vector_input)
    begin
        for i in vector_input'range loop
            if vector_input(i) = '1' then
                integer_out <= integer_out + i ** 2;
            end if;
        end loop;
    end process vector_to_int;


    int_to_vector : process(integer_input)
    begin
        if integer_input <= 2 ** vector_out'length then         
            for i in vector_out'range loop
                if integer_input >= i ** 2 then
                    vector_out(i) <= '1';
                else
                    vector_out(i) <= '0';
                end if;
            end loop;
        end if;
    end process int_to_vector;

end td1_exo2;

 
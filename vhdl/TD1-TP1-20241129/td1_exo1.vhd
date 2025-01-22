library ieee;
use ieee.std_logic_1164.all;
use IEEE.math_real.all;

package mytool is

    function td1_1_1 (input_vector : in std_logic_vector(7 downto 0))
    return integer;

    function td1_2_1 (input_vector : in std_logic_vector(7 downto 0))
    return integer;

    function td1_2_2 (input_int: in integer)
    return std_logic_vector;

end  package mytool;
package body mytool is

    function td1_1_1 (input_vector : in std_logic_vector(7 downto 0))
    return integer is
        variable r : std_logic := '0';
        variable my_output : integer := 0;
    begin
        for i in input_vector'range loop
            r := input_vector(i);
            if r = '1' then 
                return my_output;
            else 
                my_output := my_output + 1;
            end if;
        end loop;
    end;

 -- EXO1_Q2 cette fonction ne depend pas de la taille du vecteur
    
end package body mytool;
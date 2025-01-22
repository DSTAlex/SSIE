library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;


entity MyFour is 
    port(
        Clock          : in     std_logic ; -- Clock
        DoorSensor     : in     std_logic ;
        Duration       : in     std_logic_vector(15 downto 0) ;
        G_Engine       : out    std_logic ;
        HeatSetting    : in     std_logic_vector(0 to 2) ;
        MW_Engine      : out    std_logic ;
        MicroWavePower : out    std_logic_vector(0 to 1) ;
        Plate_Engine   : out    std_logic ;
        Ring           : out    std_logic ;
        StartCooker    : in     std_logic ;
        StartDefrost   : in     std_logic ;
        StartGrill     : in     std_logic ;
        StartMicroWave : in     std_logic ;
        StopOp         : in     std_logic ;
        StopPlate      : in     std_logic ;
        Thermostat     : out    std_logic_vector(0 to 2) ;
        TimeDisplay    : out    std_logic_vector(15 downto 0) ;
        nReset         : in     std_logic ) ; -- Reset
    end Myfour;

architecture td2 of MyFour is
    type state_MW is (
        idle,
        defrost_running,
        microwave_running,
        ringing,
        gril_preheating,
        wait_start_grill,
        grill_heating,
        MWG_working
    );

    signal timer : std_logic_vector(15 downto 0) := "0000000000000001" ;
    signal state : state_MW := idle;

    begin

    process (Clock, nReset)
    begin
        timer <= std_logic_vector(unsigned(timer) - 1);  
        if (nReset = '0' or StopOp = '1') then
            state <= idle;
            timer <= Duration;
            G_Engine <=  '0';
            MW_Engine <= '0';
            Ring <= '0';
            MicroWavePower  <= "11";
            Plate_Engine <= '0';
        elsif (Clock = '1') then
            case state is
                when idle =>
                    if (StartDefrost = '1') then
                        state <= defrost_running;
                        MW_Engine <= '1';
                        MicroWavePower <= "00";
                        Plate_Engine <= '1';
                    elsif (StartMicroWave = '1') then
                        state <= microwave_running;
                        MW_Engine <= '1';
                        MicroWavePower <= HeatSetting(0 to 1);
                        Plate_Engine <= '1';
                    elsif (StartGrill = '1') then
                        state <= gril_preheating;
                        G_Engine <= '1';
                        Thermostat <= HeatSetting;
                    elsif (StartCooker = '1') then
                        state <= MWG_working;
                        MW_Engine <= '1';
                        G_Engine <= '1';
                        Thermostat <= "111";
                        MicroWavePower <= HeatSetting(0 to 1);
                        Plate_Engine <= '1'; 
                    end if;
                when microwave_running =>
                    if (DoorSensor = '1') then
                        state <= idle;
                        timer <= Duration;
                        G_Engine <=  '0';
                        MW_Engine <= '0';
                        Ring <= '0';
                        MicroWavePower  <= "11";
                        Plate_Engine <= '0';
                    else
                        if (timer = "0000000000000000") then
                            state <= ringing;
                            Ring <= '1';
                        end if;
                end if;
                when defrost_running =>
                    if (DoorSensor = '1') then
                        state <= idle;
                        timer <= Duration;
                        G_Engine <=  '0';
                        MW_Engine <= '0';
                        Ring <= '0';
                        MicroWavePower  <= "11";
                        Plate_Engine <= '0';
                    else
                        if (timer = "0000000000000000") then
                            state <= ringing;
                            Ring <= '1';
                        end if;
                    end if;
                when ringing =>
                    state <= idle;
                    timer <= Duration;
                    G_Engine <=  '0';
                    MW_Engine <= '0';
                    Ring <= '0';
                    MicroWavePower  <= "11";
                    Plate_Engine <= '0';
                when gril_preheating =>
                    if (timer = "0000000000000000") then
                        state <= wait_start_grill;
                        G_Engine <= '0';
                        timer <= Duration;
                    end if;
                when wait_start_grill =>
                    if (StartGrill = '1') then
                        state <= grill_heating;
                        G_Engine <= '1';
                    end if;
                when grill_heating =>
                    if (timer = "0000000000000000") then
                        state <= ringing;
                        Ring <= '1';
                    end if;
                when MWG_working => 
                    if (DoorSensor = '1') then
                        state <= idle;
                        timer <= Duration;
                        G_Engine <=  '0';
                        MW_Engine <= '0';
                        Ring <= '0';
                        MicroWavePower  <= "11";
                        Plate_Engine <= '0';
                    else
                        if (timer = "0000000000000000") then
                            state <= ringing;
                            Ring <= '1';
                        end if;
                    end if;
            end case;
        end if;

    TimeDisplay <= timer;

    end process;

end td2;

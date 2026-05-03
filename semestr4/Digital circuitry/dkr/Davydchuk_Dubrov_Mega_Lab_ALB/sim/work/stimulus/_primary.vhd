library verilog;
use verilog.vl_types.all;
entity stimulus is
    generic(
        WIDTH           : integer := 12
    );
    port(
        A_ALB           : out    vl_logic_vector;
        B_ALB           : out    vl_logic_vector;
        CI              : out    vl_logic;
        ALB_MI          : out    vl_logic_vector(1 downto 0);
        clock           : in     vl_logic;
        resetb          : in     vl_logic
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of WIDTH : constant is 1;
end stimulus;

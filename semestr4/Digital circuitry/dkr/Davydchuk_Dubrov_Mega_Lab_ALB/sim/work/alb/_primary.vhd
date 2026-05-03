library verilog;
use verilog.vl_types.all;
entity alb is
    generic(
        WIDTH           : integer := 12
    );
    port(
        F_ALB           : out    vl_logic_vector;
        F_NORM          : out    vl_logic_vector;
        CO              : out    vl_logic;
        VO              : out    vl_logic;
        NO              : out    vl_logic;
        ZO              : out    vl_logic;
        NORM_RIGHT      : out    vl_logic;
        A_ALB           : in     vl_logic_vector;
        B_ALB           : in     vl_logic_vector;
        CI              : in     vl_logic;
        ALB_MI          : in     vl_logic_vector(1 downto 0);
        clock           : in     vl_logic;
        resetb          : in     vl_logic
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of WIDTH : constant is 1;
end alb;

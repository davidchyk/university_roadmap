library verilog;
use verilog.vl_types.all;
entity alb_ref is
    generic(
        WIDTH           : integer := 12
    );
    port(
        F_REF           : out    vl_logic_vector;
        F_NORM_REF      : out    vl_logic_vector;
        CO_REF          : out    vl_logic;
        VO_REF          : out    vl_logic;
        NO_REF          : out    vl_logic;
        ZO_REF          : out    vl_logic;
        NORM_RIGHT_REF  : out    vl_logic;
        A_ALB           : in     vl_logic_vector;
        B_ALB           : in     vl_logic_vector;
        CI              : in     vl_logic;
        ALB_MI          : in     vl_logic_vector(1 downto 0);
        clock           : in     vl_logic;
        resetb          : in     vl_logic
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of WIDTH : constant is 1;
end alb_ref;

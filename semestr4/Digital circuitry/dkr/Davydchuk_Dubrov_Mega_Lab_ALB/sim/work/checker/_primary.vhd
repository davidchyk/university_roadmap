library verilog;
use verilog.vl_types.all;
entity checker is
    generic(
        WIDTH           : integer := 12
    );
    port(
        F_ALB           : in     vl_logic_vector;
        F_NORM          : in     vl_logic_vector;
        CO              : in     vl_logic;
        VO              : in     vl_logic;
        NO              : in     vl_logic;
        ZO              : in     vl_logic;
        NORM_RIGHT      : in     vl_logic;
        F_REF           : in     vl_logic_vector;
        F_NORM_REF      : in     vl_logic_vector;
        CO_REF          : in     vl_logic;
        VO_REF          : in     vl_logic;
        NO_REF          : in     vl_logic;
        ZO_REF          : in     vl_logic;
        NORM_RIGHT_REF  : in     vl_logic;
        clock           : in     vl_logic;
        resetb          : in     vl_logic
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of WIDTH : constant is 1;
end checker;

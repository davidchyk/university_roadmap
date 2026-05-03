library verilog;
use verilog.vl_types.all;
entity top is
    generic(
        WIDTH           : integer := 12
    );
    attribute mti_svvh_generic_type : integer;
    attribute mti_svvh_generic_type of WIDTH : constant is 1;
end top;

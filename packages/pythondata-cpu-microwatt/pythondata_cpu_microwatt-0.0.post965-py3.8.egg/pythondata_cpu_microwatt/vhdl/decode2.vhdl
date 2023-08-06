library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

library work;
use work.decode_types.all;
use work.common.all;
use work.helpers.all;
use work.insn_helpers.all;

entity decode2 is
    generic (
        EX1_BYPASS : boolean := true;
        HAS_FPU : boolean := true;
        -- Non-zero to enable log data collection
        LOG_LENGTH : natural := 0
        );
    port (
        clk   : in std_ulogic;
        rst   : in std_ulogic;

        complete_in : in std_ulogic;
        busy_in   : in std_ulogic;
        stall_out : out std_ulogic;

        stopped_out : out std_ulogic;

        flush_in: in std_ulogic;

        d_in  : in Decode1ToDecode2Type;

        e_out : out Decode2ToExecute1Type;

        r_in  : in RegisterFileToDecode2Type;
        r_out : out Decode2ToRegisterFileType;

        c_in  : in CrFileToDecode2Type;
        c_out : out Decode2ToCrFileType;

        log_out : out std_ulogic_vector(9 downto 0)
	);
end entity decode2;

architecture behaviour of decode2 is
    type reg_type is record
        e : Decode2ToExecute1Type;
        repeat : std_ulogic;
    end record;

    signal r, rin : reg_type;

    signal deferred : std_ulogic;

    type decode_input_reg_t is record
        reg_valid : std_ulogic;
        reg       : gspr_index_t;
        data      : std_ulogic_vector(63 downto 0);
    end record;

    type decode_output_reg_t is record
        reg_valid : std_ulogic;
        reg       : gspr_index_t;
    end record;

    function decode_input_reg_a (t : input_reg_a_t; insn_in : std_ulogic_vector(31 downto 0);
                                 reg_data : std_ulogic_vector(63 downto 0);
                                 ispr : gspr_index_t;
                                 instr_addr : std_ulogic_vector(63 downto 0))
        return decode_input_reg_t is
    begin
        if t = RA or (t = RA_OR_ZERO and insn_ra(insn_in) /= "00000") then
            return ('1', gpr_to_gspr(insn_ra(insn_in)), reg_data);
        elsif t = SPR then
            -- ISPR must be either a valid fast SPR number or all 0 for a slow SPR.
            -- If it's all 0, we don't treat it as a dependency as slow SPRs
            -- operations are single issue.
            --
            assert is_fast_spr(ispr) =  '1' or ispr = "0000000"
                report "Decode A says SPR but ISPR is invalid:" &
                to_hstring(ispr) severity failure;
            return (is_fast_spr(ispr), ispr, reg_data);
        elsif t = CIA then
            return ('0', (others => '0'), instr_addr);
        elsif HAS_FPU and t = FRA then
            return ('1', fpr_to_gspr(insn_fra(insn_in)), reg_data);
        else
            return ('0', (others => '0'), (others => '0'));
        end if;
    end;

    function decode_input_reg_b (t : input_reg_b_t; insn_in : std_ulogic_vector(31 downto 0);
                                 reg_data : std_ulogic_vector(63 downto 0);
                                 ispr : gspr_index_t) return decode_input_reg_t is
        variable ret : decode_input_reg_t;
    begin
        case t is
            when RB =>
                ret := ('1', gpr_to_gspr(insn_rb(insn_in)), reg_data);
            when FRB =>
                if HAS_FPU then
                    ret := ('1', fpr_to_gspr(insn_frb(insn_in)), reg_data);
                else
                    ret := ('0', (others => '0'), (others => '0'));
                end if;
            when CONST_UI =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(unsigned(insn_ui(insn_in)), 64)));
            when CONST_SI =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_si(insn_in)), 64)));
            when CONST_SI_HI =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_si(insn_in)) & x"0000", 64)));
            when CONST_UI_HI =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(unsigned(insn_si(insn_in)) & x"0000", 64)));
            when CONST_LI =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_li(insn_in)) & "00", 64)));
            when CONST_BD =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_bd(insn_in)) & "00", 64)));
            when CONST_DS =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_ds(insn_in)) & "00", 64)));
            when CONST_DQ =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_dq(insn_in)) & "0000", 64)));
            when CONST_DXHI4 =>
                ret := ('0', (others => '0'), std_ulogic_vector(resize(signed(insn_dx(insn_in)) & x"0004", 64)));
            when CONST_M1 =>
                ret := ('0', (others => '0'), x"FFFFFFFFFFFFFFFF");
            when CONST_SH =>
                ret := ('0', (others => '0'), x"00000000000000" & "00" & insn_in(1) & insn_in(15 downto 11));
            when CONST_SH32 =>
                ret := ('0', (others => '0'), x"00000000000000" & "000" & insn_in(15 downto 11));
            when SPR =>
                -- ISPR must be either a valid fast SPR number or all 0 for a slow SPR.
                -- If it's all 0, we don't treat it as a dependency as slow SPRs
                -- operations are single issue.
                assert is_fast_spr(ispr) = '1' or ispr = "0000000"
                    report "Decode B says SPR but ISPR is invalid:" &
                    to_hstring(ispr) severity failure;
                ret := (is_fast_spr(ispr), ispr, reg_data);
            when NONE =>
                ret := ('0', (others => '0'), (others => '0'));
        end case;

        return ret;
    end;

    function decode_input_reg_c (t : input_reg_c_t; insn_in : std_ulogic_vector(31 downto 0);
                                 reg_data : std_ulogic_vector(63 downto 0)) return decode_input_reg_t is
    begin
        case t is
            when RS =>
                return ('1', gpr_to_gspr(insn_rs(insn_in)), reg_data);
            when RCR =>
                return ('1', gpr_to_gspr(insn_rcreg(insn_in)), reg_data);
            when FRS =>
                if HAS_FPU then
                    return ('1', fpr_to_gspr(insn_frt(insn_in)), reg_data);
                else
                    return ('0', (others => '0'), (others => '0'));
                end if;
            when FRC =>
                if HAS_FPU then
                    return ('1', fpr_to_gspr(insn_frc(insn_in)), reg_data);
                else
                    return ('0', (others => '0'), (others => '0'));
                end if;
            when NONE =>
                return ('0', (others => '0'), (others => '0'));
        end case;
    end;

    function decode_output_reg (t : output_reg_a_t; insn_in : std_ulogic_vector(31 downto 0);
                                ispr : gspr_index_t) return decode_output_reg_t is
    begin
        case t is
            when RT =>
                return ('1', gpr_to_gspr(insn_rt(insn_in)));
            when RA =>
                return ('1', gpr_to_gspr(insn_ra(insn_in)));
            when FRT =>
                if HAS_FPU then
                    return ('1', fpr_to_gspr(insn_frt(insn_in)));
                else
                    return ('0', "0000000");
                end if;
            when SPR =>
                -- ISPR must be either a valid fast SPR number or all 0 for a slow SPR.
                -- If it's all 0, we don't treat it as a dependency as slow SPRs
                -- operations are single issue.
                assert is_fast_spr(ispr) = '1' or ispr = "0000000"
                    report "Decode B says SPR but ISPR is invalid:" &
                    to_hstring(ispr) severity failure;
                return (is_fast_spr(ispr), ispr);
            when NONE =>
                return ('0', "0000000");
        end case;
    end;

    function decode_rc (t : rc_t; insn_in : std_ulogic_vector(31 downto 0)) return std_ulogic is
    begin
        case t is
            when RC =>
                return insn_rc(insn_in);
            when ONE =>
                return '1';
            when NONE =>
                return '0';
        end case;
    end;

    -- For now, use "rc" in the decode table to decide whether oe exists.
    -- This is not entirely correct architecturally: For mulhd and
    -- mulhdu, the OE field is reserved. It remains to be seen what an
    -- actual POWER9 does if we set it on those instructions, for now we
    -- test that further down when assigning to the multiplier oe input.
    --
    function decode_oe (t : rc_t; insn_in : std_ulogic_vector(31 downto 0)) return std_ulogic is
    begin
        case t is
            when RC =>
                return insn_oe(insn_in);
            when OTHERS =>
                return '0';
        end case;
    end;

    -- control signals that are derived from insn_type
    type mux_select_array_t is array(insn_type_t) of std_ulogic_vector(2 downto 0);

    constant result_select : mux_select_array_t := (
        OP_AND      => "001",           -- logical_result
        OP_OR       => "001",
        OP_XOR      => "001",
        OP_POPCNT   => "001",
        OP_PRTY     => "001",
        OP_CMPB     => "001",
        OP_EXTS     => "001",
        OP_BPERM    => "001",
        OP_BCD      => "001",
        OP_MTSPR    => "001",
        OP_RLC      => "010",           -- rotator_result
        OP_RLCL     => "010",
        OP_RLCR     => "010",
        OP_SHL      => "010",
        OP_SHR      => "010",
        OP_EXTSWSLI => "010",
        OP_MUL_L64  => "011",           -- muldiv_result
        OP_MUL_H64  => "011",
        OP_MUL_H32  => "011",
        OP_DIV      => "011",
        OP_DIVE     => "011",
        OP_MOD      => "011",
        OP_CNTZ     => "100",           -- countzero_result
        OP_MFSPR    => "101",           -- spr_result
        OP_ADDG6S   => "111",           -- misc_result
        OP_ISEL     => "111",
        OP_DARN     => "111",
        OP_MFMSR    => "111",
        OP_MFCR     => "111",
        OP_SETB     => "111",
        others      => "000"            -- default to adder_result
        );

    constant subresult_select : mux_select_array_t := (
        OP_MUL_L64 => "000",            -- muldiv_result
        OP_MUL_H64 => "001",
        OP_MUL_H32 => "010",
        OP_DIV     => "011",
        OP_DIVE    => "011",
        OP_MOD     => "011",
        OP_ADDG6S  => "001",            -- misc_result
        OP_ISEL    => "010",
        OP_DARN    => "011",
        OP_MFMSR   => "100",
        OP_MFCR    => "101",
        OP_SETB    => "110",
        others     => "000"
        );

    -- issue control signals
    signal control_valid_in : std_ulogic;
    signal control_valid_out : std_ulogic;
    signal control_stall_out : std_ulogic;
    signal control_sgl_pipe : std_logic;

    signal gpr_write_valid : std_ulogic;
    signal gpr_write : gspr_index_t;
    signal gpr_bypassable  : std_ulogic;

    signal update_gpr_write_valid : std_ulogic;
    signal update_gpr_write_reg : gspr_index_t;

    signal gpr_a_read_valid : std_ulogic;
    signal gpr_a_read :gspr_index_t;
    signal gpr_a_bypass : std_ulogic;

    signal gpr_b_read_valid : std_ulogic;
    signal gpr_b_read : gspr_index_t;
    signal gpr_b_bypass : std_ulogic;

    signal gpr_c_read_valid : std_ulogic;
    signal gpr_c_read : gspr_index_t;
    signal gpr_c_bypass : std_ulogic;

    signal cr_write_valid  : std_ulogic;
    signal cr_bypass       : std_ulogic;
    signal cr_bypass_avail : std_ulogic;

begin
    control_0: entity work.control
	generic map (
            PIPELINE_DEPTH => 1
            )
	port map (
            clk         => clk,
            rst         => rst,

            complete_in => complete_in,
            valid_in    => control_valid_in,
            repeated    => r.repeat,
            busy_in     => busy_in,
            deferred    => deferred,
            flush_in    => flush_in,
            sgl_pipe_in => control_sgl_pipe,
            stop_mark_in => d_in.stop_mark,

            gpr_write_valid_in => gpr_write_valid,
            gpr_write_in       => gpr_write,
            gpr_bypassable     => gpr_bypassable,

            update_gpr_write_valid => update_gpr_write_valid,
            update_gpr_write_reg => update_gpr_write_reg,

            gpr_a_read_valid_in  => gpr_a_read_valid,
            gpr_a_read_in        => gpr_a_read,

            gpr_b_read_valid_in  => gpr_b_read_valid,
            gpr_b_read_in        => gpr_b_read,

            gpr_c_read_valid_in  => gpr_c_read_valid,
            gpr_c_read_in        => gpr_c_read,

            cr_read_in           => d_in.decode.input_cr,
            cr_write_in          => cr_write_valid,
            cr_bypass            => cr_bypass,
            cr_bypassable        => cr_bypass_avail,

            valid_out   => control_valid_out,
            stall_out   => control_stall_out,
            stopped_out => stopped_out,

            gpr_bypass_a => gpr_a_bypass,
            gpr_bypass_b => gpr_b_bypass,
            gpr_bypass_c => gpr_c_bypass
            );

    deferred <= r.e.valid and busy_in;

    decode2_0: process(clk)
    begin
        if rising_edge(clk) then
            if rst = '1' or flush_in = '1' or deferred = '0' then
                if rin.e.valid = '1' then
                    report "execute " & to_hstring(rin.e.nia);
                end if;
                r <= rin;
            end if;
        end if;
    end process;

    c_out.read <= d_in.decode.input_cr;

    decode2_1: process(all)
        variable v : reg_type;
        variable mul_a : std_ulogic_vector(63 downto 0);
        variable mul_b : std_ulogic_vector(63 downto 0);
        variable decoded_reg_a : decode_input_reg_t;
        variable decoded_reg_b : decode_input_reg_t;
        variable decoded_reg_c : decode_input_reg_t;
        variable decoded_reg_o : decode_output_reg_t;
        variable length : std_ulogic_vector(3 downto 0);
    begin
        v := r;

        v.e := Decode2ToExecute1Init;

        mul_a := (others => '0');
        mul_b := (others => '0');

        --v.e.input_cr := d_in.decode.input_cr;
        v.e.output_cr := d_in.decode.output_cr;
        
        decoded_reg_a := decode_input_reg_a (d_in.decode.input_reg_a, d_in.insn, r_in.read1_data, d_in.ispr1,
                                             d_in.nia);
        decoded_reg_b := decode_input_reg_b (d_in.decode.input_reg_b, d_in.insn, r_in.read2_data, d_in.ispr2);
        decoded_reg_c := decode_input_reg_c (d_in.decode.input_reg_c, d_in.insn, r_in.read3_data);
        decoded_reg_o := decode_output_reg (d_in.decode.output_reg_a, d_in.insn, d_in.ispr1);

        if d_in.decode.repeat /= NONE then
            v.e.repeat := '1';
            v.e.second := r.repeat;
            case d_in.decode.repeat is
                when DRSE =>
                    -- do RS|1,RS for LE; RS,RS|1 for BE
                    if r.repeat = d_in.big_endian then
                        decoded_reg_c.reg(0) := '1';
                    end if;
                when DRTE =>
                    -- do RT|1,RT for LE; RT,RT|1 for BE
                    if r.repeat = d_in.big_endian then
                        decoded_reg_o.reg(0) := '1';
                    end if;
                when others =>
            end case;
        end if;

        r_out.read1_enable <= decoded_reg_a.reg_valid and d_in.valid;
        r_out.read1_reg    <= decoded_reg_a.reg;
        r_out.read2_enable <= decoded_reg_b.reg_valid and d_in.valid;
        r_out.read2_reg    <= decoded_reg_b.reg;
        r_out.read3_enable <= decoded_reg_c.reg_valid and d_in.valid;
        r_out.read3_reg    <= decoded_reg_c.reg;

        case d_in.decode.length is
            when is1B =>
                length := "0001";
            when is2B =>
                length := "0010";
            when is4B =>
                length := "0100";
            when is8B =>
                length := "1000";
            when NONE =>
                length := "0000";
        end case;

        -- execute unit
        v.e.nia := d_in.nia;
        v.e.unit := d_in.decode.unit;
        v.e.fac := d_in.decode.facility;
        v.e.insn_type := d_in.decode.insn_type;
        v.e.read_reg1 := decoded_reg_a.reg;
        v.e.read_data1 := decoded_reg_a.data;
        v.e.bypass_data1 := gpr_a_bypass;
        v.e.read_reg2 := decoded_reg_b.reg;
        v.e.read_data2 := decoded_reg_b.data;
        v.e.bypass_data2 := gpr_b_bypass;
        v.e.read_data3 := decoded_reg_c.data;
        v.e.bypass_data3 := gpr_c_bypass;
        v.e.write_reg := decoded_reg_o.reg;
        v.e.write_reg_enable := decoded_reg_o.reg_valid;
        v.e.rc := decode_rc(d_in.decode.rc, d_in.insn);
        if not (d_in.decode.insn_type = OP_MUL_H32 or d_in.decode.insn_type = OP_MUL_H64) then
            v.e.oe := decode_oe(d_in.decode.rc, d_in.insn);
        end if;
        v.e.cr := c_in.read_cr_data;
        v.e.bypass_cr := cr_bypass;
        v.e.xerc := c_in.read_xerc_data;
        v.e.invert_a := d_in.decode.invert_a;
        v.e.addm1 := '0';
        if d_in.decode.insn_type = OP_BC or d_in.decode.insn_type = OP_BCREG then
            -- add -1 to CTR
            v.e.addm1 := '1';
            if d_in.insn(23) = '1' or
                (d_in.decode.insn_type = OP_BCREG and d_in.insn(10) = '0') then
                -- don't write decremented CTR if BO(2) = 1 or bcctr
                v.e.write_reg_enable := '0';
            end if;
        end if;
        v.e.invert_out := d_in.decode.invert_out;
        v.e.input_carry := d_in.decode.input_carry;
        v.e.output_carry := d_in.decode.output_carry;
        v.e.is_32bit := d_in.decode.is_32bit;
        v.e.is_signed := d_in.decode.is_signed;
        if d_in.decode.lr = '1' then
            v.e.lr := insn_lk(d_in.insn);
        end if;
        v.e.insn := d_in.insn;
        v.e.data_len := length;
        v.e.byte_reverse := d_in.decode.byte_reverse;
        v.e.sign_extend := d_in.decode.sign_extend;
        v.e.update := d_in.decode.update;
        v.e.reserve := d_in.decode.reserve;
        v.e.br_pred := d_in.br_pred;
        v.e.result_sel := result_select(d_in.decode.insn_type);
        v.e.sub_select := subresult_select(d_in.decode.insn_type);

        -- issue control
        control_valid_in <= d_in.valid;
        control_sgl_pipe <= d_in.decode.sgl_pipe;

        gpr_write_valid <= v.e.write_reg_enable;
        gpr_write <= decoded_reg_o.reg;
        gpr_bypassable <= '0';
        if EX1_BYPASS and d_in.decode.unit = ALU then
            gpr_bypassable <= '1';
        end if;
        update_gpr_write_valid <= d_in.decode.update;
        update_gpr_write_reg <= decoded_reg_a.reg;
        if v.e.lr = '1' then
            -- there are no instructions that have both update=1 and lr=1
            update_gpr_write_valid <= '1';
            update_gpr_write_reg <= fast_spr_num(SPR_LR);
        end if;

        gpr_a_read_valid <= decoded_reg_a.reg_valid;
        gpr_a_read <= decoded_reg_a.reg;

        gpr_b_read_valid <= decoded_reg_b.reg_valid;
        gpr_b_read <= decoded_reg_b.reg;

        gpr_c_read_valid <= decoded_reg_c.reg_valid;
        gpr_c_read <= decoded_reg_c.reg;

        cr_write_valid <= d_in.decode.output_cr or decode_rc(d_in.decode.rc, d_in.insn);
        cr_bypass_avail <= '0';
        if EX1_BYPASS and d_in.decode.unit = ALU then
            cr_bypass_avail <= d_in.decode.output_cr;
        end if;

        v.e.valid := control_valid_out;
        if control_valid_out = '1' then
            v.repeat := v.e.repeat and not r.repeat;
        end if;

        stall_out <= control_stall_out or v.repeat;

        if rst = '1' or flush_in = '1' then
            v.e := Decode2ToExecute1Init;
            v.repeat := '0';
        end if;

        -- Update registers
        rin <= v;

        -- Update outputs
        e_out <= r.e;
    end process;

    d2_log: if LOG_LENGTH > 0 generate
        signal log_data : std_ulogic_vector(9 downto 0);
    begin
        dec2_log : process(clk)
        begin
            if rising_edge(clk) then
                log_data <= r.e.nia(5 downto 2) &
                            r.e.valid &
                            stopped_out &
                            stall_out &
                            r.e.bypass_data3 &
                            r.e.bypass_data2 &
                            r.e.bypass_data1;
            end if;
        end process;
        log_out <= log_data;
    end generate;

end architecture behaviour;

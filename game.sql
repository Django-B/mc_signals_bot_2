CREATE TABLE IF NOT EXISTS game (
    id integer primary key autoincrement,
    game_id integer unique,

    game_date text,
    game_time text,

    p1_name text,
    p2_name text,

    p1_game_win_coef real,
    p2_game_win_coef real,

    p1_round_win_coef real,
    p2_round_win_coef real,

    f_coef real,
    b_coef real,
    r_coef real,

    min_num_total real,
    mid_num_total real,
    max_num_total real,

    min_num_total_min_coef real,
    min_num_total_max_coef real,

    mid_num_total_min_coef real,
    mid_num_total_max_coef real,

    max_num_total_min_coef real,
    max_num_total_max_coef real,

    fyes real,
    fno real,

    p1_wins integer,
    p2_wins integer,

    round1_winner text,
    round1_finish text,
    round1_time text,
    round1_total text,

    round2_winner text,
    round2_finish text,
    round2_time text,
    round2_total text,

    round3_winner text,
    round3_finish text,
    round3_time text,
    round3_total text,

    round4_winner text,
    round4_finish text,
    round4_time text,
    round4_total text,

    round5_winner text,
    round5_finish text,
    round5_time text,
    round5_total text,

    round6_winner text,
    round6_finish text,
    round6_time text,
    round6_total text,

    round7_winner text,
    round7_finish text,
    round7_time text,
    round7_total text,

    round8_winner text,
    round8_finish text,
    round8_time text,
    round8_total text,

    round9_winner text,
    round9_finish text,
    round9_time text,
    round9_total text
);

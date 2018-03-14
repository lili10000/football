-- create table if not exists k_corner(
--     main VARCHAR(255),
--     client VARCHAR(255),
--     main_score INT,
--     client_score INT,
--     rate VARCHAR(255),
--     type VARCHAR(255),
--     main_corner INT,
-- 	client_corner INT,
--     sum_corner INT);

create table if not exists k_rate(
    id INT,
    main VARCHAR(255),
    client VARCHAR(255),
    main_score INT,
    client_score INT,
    type VARCHAR(255),
    start_win_rate VARCHAR(255),
	start_ping_rate VARCHAR(255),
    start_lost_rate VARCHAR(255),
    end_win_rate VARCHAR(255),
    end_ping_rate VARCHAR(255),
    end_lost_rate VARCHAR(255),
    PRIMARY KEY (id));
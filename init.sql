-- init.sql

CREATE TABLE
    IF NOT EXISTS ita_table (
        id SERIAL PRIMARY KEY,
        code integer,
        pDPP numeric(6, 1),
        pDV integer,
        pPRP numeric(6, 1),
        pDOP numeric(6, 1),
        pDHP numeric(6, 1),
        pDLP numeric(6, 1),
        pVWAP numeric(11, 4),
        pQAP numeric(6, 1),
        pQAS numeric(6, 1),
        pQBP numeric(6, 1),
        pQBS numeric(6, 1),
        pAAV integer,
        pABV numeric(6, 1),
        pQOV integer,
        pQUV integer,
        pGAP10 numeric(6, 1),
        pGAP9 numeric(6, 1),
        pGAP8 numeric(6, 1),
        pGAP7 numeric(6, 1),
        pGAP6 numeric(6, 1),
        pGAP5 numeric(6, 1),
        pGAP4 numeric(6, 1),
        pGAP3 numeric(6, 1),
        pGAP2 numeric(6, 1),
        pGAP1 numeric(6, 1),
        pGBP10 numeric(6, 1),
        pGBP9 numeric(6, 1),
        pGBP8 numeric(6, 1),
        pGBP7 numeric(6, 1),
        pGBP6 numeric(6, 1),
        pGBP5 numeric(6, 1),
        pGBP4 numeric(6, 1),
        pGBP3 numeric(6, 1),
        pGBP2 numeric(6, 1),
        pGBP1 numeric(6, 1),
        pGAV10 integer,
        pGAV9 integer,
        pGAV8 integer,
        pGAV7 integer,
        pGAV6 integer,
        pGAV5 integer,
        pGAV4 integer,
        pGAV3 integer,
        pGAV2 integer,
        pGAV1 integer,
        pGBV10 integer,
        pGBV9 integer,
        pGBV8 integer,
        pGBV7 integer,
        pGBV6 integer,
        pGBV5 integer,
        pGBV4 integer,
        pGBV3 integer,
        pGBV2 integer,
        pGBV1 integer,
        created_at timestamp(6)
        with
            time zone DEFAULT NOW(),
            updated_at timestamp(6)
        with
            time zone DEFAULT NOW()
    );

-- CODE列にインデックスを作成

CREATE INDEX idx_ita_table_code ON ita_table (code);

-- created_at列にインデックスを作成

CREATE INDEX idx_ita_table_created_at ON ita_table (created_at);

CREATE TABLE
    master_stock_table (
        code integer PRIMARY KEY,
        name VARCHAR(255),
        market_product_category VARCHAR(225),
        sector33_code integer,
        sector33_category VARCHAR(255),
        sector17_code integer,
        sector17_category VARCHAR(255),
        scale_code integer,
        scale_category VARCHAR(255),
        api_id VARCHAR(255),
        created_at timestamp DEFAULT current_timestamp,
        updated_at timestamp DEFAULT current_timestamp
    );

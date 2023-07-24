-- init.sql
CREATE TABLE IF NOT EXISTS ita_table (
  id SERIAL PRIMARY KEY,
  code integer,
  pDPP numeric(6, 1),
  pDV integer,
  pPRP numeric(6, 1),
  pDOP numeric(6, 1),
  pDHP numeric(6, 1),
  pDLP numeric(6, 1),
  pVWAP numeric(6, 1),
  pQAP numeric(6, 1),
  pQAS numeric(6, 1),
  pQBP integer,
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
  created_at timestamp(6) with time zone DEFAULT NOW(),
  updated_at timestamp(6) with time zone DEFAULT NOW()
);


-- CODE列にインデックスを作成
CREATE INDEX idx_ita_table_code ON ita_table (code);

-- created_at列にインデックスを作成
CREATE INDEX idx_ita_table_created_at ON ita_table (created_at);

-- デモデータの挿入
INSERT INTO ita_table (code, pDPP, pDV, pPRP, pDOP, pDHP, pDLP, pVWAP, pQAP, pQAS, pQBP, pQBS, pAAV, pABV, pQOV, pQUV, pGAP10, pGAP9, pGAP8, pGAP7, pGAP6, pGAP5, pGAP4, pGAP3, pGAP2, pGAP1, pGBP10, pGBP9, pGBP8, pGBP7, pGBP6, pGBP5, pGBP4, pGBP3, pGBP2, pGBP1, pGAV10, pGAV9, pGAV8, pGAV7, pGAV6, pGAV5, pGAV4, pGAV3, pGAV2, pGAV1, pGBV10, pGBV9, pGBV8, pGBV7, pGBV6, pGBV5, pGBV4, pGBV3, pGBV2, pGBV1, created_at)
VALUES
  (1234, 1.2, 100, 2.3, 4.5, 6.7, 8.9, 10.1, 12.3, 14.5, 16, 18.2, 200, 22.4, 240, 26, 28.1, 3.1, 4.2, 5.3, 6.4, 7.5, 8.6, 9.7, 10.8, 11.9, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, '2023-07-25 12:00:00+00:00'),
  (1235, 1.2, 100, 2.3, 4.5, 6.7, 8.9, 10.1, 12.3, 14.5, 16, 18.2, 200, 22.4, 240, 26, 28.1, 3.1, 4.2, 5.3, 6.4, 7.5, 8.6, 9.7, 10.8, 11.9, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, '2023-07-25 12:00:00+00:00'),
  (1236, 1.2, 100, 2.3, 4.5, 6.7, 8.9, 10.1, 12.3, 14.5, 16, 18.2, 200, 22.4, 240, 26, 28.1, 3.1, 4.2, 5.3, 6.4, 7.5, 8.6, 9.7, 10.8, 11.9, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, '2023-07-25 12:00:00+00:00');

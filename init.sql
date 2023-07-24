-- init.sql
CREATE TABLE ita_table (
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
  updated_at timestamp(6) with time zone DEFAULT NOW(),
);


-- CODE列にインデックスを作成
CREATE INDEX idx_ita_table_code ON ita_table (CODE);

-- created_at列にインデックスを作成
CREATE INDEX idx_ita_table_created_at ON ita_table (created_at);

-- データの挿入
INSERT INTO ita_table (CODE, pDPP, pDV, pPRP, pDOP, pDHP, pDLP, pVWAP, pQAP, pQAS, pQBP, pQBS, pAAV, pABV, pQOV, pQUV, pGAP10, pGAP9, pGAP8, pGAP7, pGAP6, pGAP5, pGAP4, pGAP3, pGAP2, pGAP1, pGBP10, pGBP9, pGBP8, pGBP7, pGBP6, pGBP5, pGBP4, pGBP3, pGBP2, pGBP1, pGAV10, pGAV9, pGAV8, pGAV7, pGAV6, pGAV5, pGAV4, pGAV3, pGAV2, pGAV1, pGBV10, pGBV9, pGBV8, pGBV7, pGBV6, pGBV5, pGBV4, pGBV3, pGBV2, pGBV1, created_at, updated_at)
VALUES
  (1234, 1.2, 100, 2.3, 4.5, 6.7, 8.9, 10.1, 12.3, 14.5, 16, 18.2, 200, 22.4, 240, 26, 28.1, 3.1, 4.2, 5.3, 6.4, 7.5, 8.6, 9.7, 10.8, 11.9, 1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9, 10.0, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, '2023-07-25 12:00:00+00:00', '2023-07-25 12:00:00+00:00'),
  (5678, 2.1, 200, 3.4, 5.6, 7.8, 9.0, 11.2, 13.4, 15.6, 17, 19.2, 300, 23.4, 340, 36, 38.1, 4.1, 5.2, 6.3, 7.4, 8.5, 9.6, 10.7, 11.8, 12.9, 2.1, 3.2, 4.3, 5.4, 6.5, 7.6, 8.7, 9.8, 10.9, 20.0, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, '2023-07-26 09:30:00+00:00', '2023-07-26 09:30:00+00:00'),
  (9101, 3.0, 300, 4.5, 6.7, 8.9, 1.1, 13.3, 15.5, 17.7, 19, 21.2, 400, 25.4, 440, 46, 48.1, 5.1, 6.2, 7.3, 8.4, 9.5, 1.6, 11.7, 12.8, 13.9, 3.1, 4.2, 5.3, 6.4, 7.5, 8.6, 9.7, 10.8, 11.9, 22.0, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, '2023-07-27 15:45:00+00:00', '2023-07-27 15:45:00+00:00'),
  (1213, 4.2, 400, 5.6, 7.8, 9.0, 1.2, 14.4, 16.6, 18.8, 20, 22.2, 500, 26.4, 540, 56, 58.1, 6.1, 7.2, 8.3, 9.4, 1.5, 2.6, 12.7, 13.8, 14.9, 4.1, 5.2, 6.3, 7.4, 8.5, 9.6, 10.7, 11.8, 12.9, 23.0, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, '2023-07-28 21:15:00+00:00', '2023-07-28 21:15:00+00:00'),
  (1415, 5.3, 500, 6.7, 8.9, 1.1, 2.3, 15.5, 17.7, 19.9, 21, 23.2, 600, 27.4, 640, 66, 68.1, 7.1, 8.2, 9.3, 1.4, 2.5, 3.6, 13.7, 14.8, 15.9, 5.1, 6.2, 7.3, 8.4, 9.5, 1.6, 10.7, 11.8, 12.9, 24.0, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, '2023-07-29 18:20:00+00:00', '2023-07-29 18:20:00+00:00');

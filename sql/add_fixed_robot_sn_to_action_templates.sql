-- Supabase：在「動作範本」表新增欄位（執行一次即可）
-- 用於：每個範本只對應一台機器人 API 時，填寫該台 SN；操作頁勾選四台就只跑四個範本。

alter table robot.showroom_action_templates
  add column if not exists fixed_robot_sn text;

comment on column robot.showroom_action_templates.fixed_robot_sn is
  '若填寫機器 SN：按鈕執行時此範本只對該台打一次，且僅在操作頁有勾選該 SN 時執行。留空則對每台勾選機器人各執行一次。';

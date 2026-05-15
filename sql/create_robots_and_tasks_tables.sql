-- 建立 robots 表格
CREATE TABLE robots (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'offline',
    battery INT DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 建立 tasks 表格
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    room_number TEXT NOT NULL,
    item TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    robot_id UUID NOT NULL REFERENCES robots(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- 建立索引以提高查詢效能
CREATE INDEX idx_tasks_robot_id ON tasks(robot_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_robots_status ON robots(status);

-- 啟用 RLS (行級安全政策) - 根據需要配置
ALTER TABLE robots ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;

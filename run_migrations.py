from alembic.config import Config
from alembic import command
import os

def run_migrations():
    # 指定 Alembic 配置文件的位置
    alembic_cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    
    # alembic revision --autogenerate -m "描述迁移的内容"
    message = "update table map_points comments" 
    command.revision(alembic_cfg, autogenerate=True, message=message)

    # alembic upgrade head
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    run_migrations()

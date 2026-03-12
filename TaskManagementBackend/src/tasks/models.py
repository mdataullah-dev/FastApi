from sqlalchemy import Column , Integer , String , Boolean , ForeignKey
from src.utils.db import Base

class TaskModel(Base):
    __tablename__ = "user_tasks"
    
    id = Column(Integer , primary_key=True)
    title = Column(String)
    description = Column(String)
    is_completed = Column(Boolean, default=False)
    
    user_id = Column(Integer , ForeignKey("user_table.id", ondelete="CASCADE"))
    #? isse connect ho gya [one-to-many relationship] user_table ki id connect kr rahe hum is task table mein
    #? cascade means => connected => meanns jitne v task is particular user se connect hongein => user delete hone ke baad vo v delete ho jayegngein
    
    
#? Model is created => ye humne jo table banaya hai ye sync ho chuka hai hamare database ke sath 
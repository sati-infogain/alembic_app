from sqlalchemy.orm import Session

from models.flow import Flow


def create_flow(db: Session, name: str, description: str = None):
    new_flow = Flow(name=name, description=description)
    db.add(new_flow)
    db.commit()
    db.refresh(new_flow)
    return new_flow

def get_flows(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Flow).offset(skip).limit(limit).all()

def get_flow(db: Session, flow_id):
    return db.query(Flow).filter(Flow.id == flow_id).first()

def delete_flow(db: Session, flow_id):
    flow = db.query(Flow).filter(Flow.id == flow_id).first()
    if not flow:
        return False
    db.delete(flow)
    db.commit()
    return True
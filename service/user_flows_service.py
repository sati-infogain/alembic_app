from models.user_flows import user_flows


def create_user_flow(db, user_id, flow_id, permission=None):
    exists = db.execute(
        user_flows.select().where(
            (user_flows.c.user_id == user_id) &
            (user_flows.c.flow_id == flow_id)
        )
    ).first()
    if exists:
        return False
    db.execute(
        user_flows.insert().values(
            user_id=user_id,
            flow_id=flow_id,
            permission=permission,
            created_at=None,
            updated_at=None,
        )
    )
    db.commit()
    return True

def get_user_flows(db):
    result = db.execute(user_flows.select()).mappings().all()
    return result

def delete_user_flow(db, user_id, flow_id):
    result = db.execute(
        user_flows.delete().where(
            (user_flows.c.user_id == user_id) &
            (user_flows.c.flow_id == flow_id)
        )
    )
    db.commit()
    return result.rowcount > 0
from db_connection import *
from models.users import User


def user_exists(self):
    row = session.query(User).filter_by(did=self).first()
    return True if row else False


def user_get(self):
    row = session.query(User).filter_by(did=self).first()
    return row


def user_create(discord_id, discord_name, score=0, reactions_triggered=0):
    user = User(did=discord_id, dname=discord_name, score=score,
                reactions_triggered=reactions_triggered)
    session.add(user)
    session.flush()
    print("Posted user to DB | {}: {}".format(discord_id, discord_name))


def increment_score(inc_score):
    session.query(User).update({User.score: User.score + inc_score})
    session.commit()


def reduce_score(red_score):
    session.query(User).update({User.score: User.score - red_score})
    session.commit()


def multiply_score(multi_score):
    session.query(User).update({User.score: User.score * multi_score})
    session.commit()


def increment_reaction_counter(self, inc_score):
    session.query(User).filter_by(did=self).update(
        {User.reactions_triggered: User.reactions_triggered + inc_score})
    session.commit()
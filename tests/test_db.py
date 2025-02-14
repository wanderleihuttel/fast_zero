from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(
        username='wanderlei',
        email='wanderlei.huttel@gmail.com',
        password=12346,
    )
    session.add(user)
    session.commit()
    result = session.scalar(
        select(User).where(User.email == 'wanderlei.huttel@gmail.com')
    )

    assert result.username == 'wanderlei'
